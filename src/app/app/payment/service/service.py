from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Final
from uuid import UUID

from app.app.common.dto.money import MoneyMapper
from app.app.payment.port import (
    PaymentMethodGateway,
    PaymentMethodGatewayError,
    PaymentMethodGatewayFactory,
)
from app.app.payment.port.payment import CancelInvoice, CreateInvoice, Invoice
from app.domain.common.actor import UserActor
from app.domain.common.money import Money
from app.domain.common.port import Clock
from app.domain.payment.entity import Payment
from app.domain.payment.enums import PaymentMethod
from app.domain.payment.exception import PaymentNotFoundError
from app.domain.payment.port import PaymentCommissionRuleRepository, PaymentRepository
from app.domain.payment.service import PaymentDomainService
from app.domain.payment.value_object import PaymentExternalId, PaymentId, PaymentPurpose

_DEFAULT_EXPIRES_IN: Final[timedelta] = timedelta(hours=3)


@dataclass(slots=True, frozen=True)
class SuccessfullyCreatedPayment:
    payment: Payment
    invoice: Invoice


@dataclass(slots=True, frozen=True)
class FailedCreatedPayment:
    payment: Payment
    e: PaymentMethodGatewayError


@dataclass(slots=True, frozen=True)
class CreatePaymentData:
    actor: UserActor
    purpose: PaymentPurpose
    method: PaymentMethod
    amount: Money

    expires_in: timedelta = _DEFAULT_EXPIRES_IN


@dataclass(slots=True, frozen=True)
class CancelPaymentData:
    id: UUID


type CreatedPayment = SuccessfullyCreatedPayment | FailedCreatedPayment


class PaymentApplicationService:
    def __init__(
        self,
        service: PaymentDomainService,
        repo: PaymentRepository,
        commission_repo: PaymentCommissionRuleRepository,
        gw_factory: PaymentMethodGatewayFactory,
        clock: Clock,
    ):
        self._service = service
        self._repo = repo
        self._commission_repo = commission_repo
        self._gw_factory = gw_factory
        self._clock = clock

    async def create(self, data: CreatePaymentData) -> CreatedPayment:
        payment: Payment = self._service.create(
            creator_id=data.actor.id,
            purpose=data.purpose,
            method=data.method,
            amount=data.amount,
            commission_rule=await self._commission_repo.get(method=data.method),
        )
        await self._repo.add(payment=payment)
        now: datetime = self._clock.now()

        try:
            gateway: PaymentMethodGateway = await self._gw_factory.get(
                method=data.method
            )
            invoice: Invoice = await gateway.create(
                data=CreateInvoice(
                    payment_id=payment.id.value,
                    to_pay=MoneyMapper.to_dto(src=payment.to_pay),
                    expires_in=data.expires_in,
                )
            )
        except PaymentMethodGatewayError as e:
            payment.fail(now=now)
            return FailedCreatedPayment(payment=payment, e=e)

        payment.start(
            external_id=PaymentExternalId(
                value=invoice.invoice_id,
            ),
            now=now,
        )

        return SuccessfullyCreatedPayment(payment=payment, invoice=invoice)

    async def cancel(self, data: CancelPaymentData) -> Payment:
        payment: Payment | None = await self._repo.acquire(
            payment_id=PaymentId(data.id),
        )
        if not payment:
            raise PaymentNotFoundError

        payment.cancel(now=self._clock.now())

        gateway = await self._gw_factory.get(payment.method)

        if payment.external_id:
            await gateway.cancel(
                data=CancelInvoice(invoice_id=payment.external_id.value)
            )

        return payment
