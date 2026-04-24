import asyncio
from asyncio import Task
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from app.common.port import DatabaseSession, TelegramNotification
from app.common.port.telegram_notification import NotificationRequest
from app.payment.dto.payment import PaymentMapper
from app.payment.exception import PaymentNotFound
from app.payment.port import (
    PaymentMethodGatewayFactory,
    PaymentPurposeHandler,
    PaymentPurposeHandlersRegistry,
)
from app.payment.port.payment.dto import GetInvoice, Invoice, InvoiceStatus
from domain.common.port import Clock
from domain.payment.entity import Payment
from domain.payment.exception import PaymentCheckForbidden
from domain.payment.port import PaymentRepository
from domain.payment.value_object import PaymentId


@dataclass(slots=True, frozen=True)
class CheckPaymentCmd:
    id: UUID


class CheckPayment:
    def __init__(
        self,
        repo: PaymentRepository,
        session: DatabaseSession,
        clock: Clock,
        factory: PaymentMethodGatewayFactory,
        notification: TelegramNotification,
        handlers_registry: PaymentPurposeHandlersRegistry,
    ):
        self._repo: PaymentRepository = repo
        self._session: DatabaseSession = session
        self._clock: Clock = clock
        self._factory: PaymentMethodGatewayFactory = factory
        self._handlers_registry: PaymentPurposeHandlersRegistry = (
            handlers_registry
        )
        self._notification: TelegramNotification = notification
        self._tasks: set[Task[Any]] = set()

    async def __call__(self, cmd: CheckPaymentCmd) -> Invoice:
        payment: Payment | None = await self._repo.get(
            payment_id=PaymentId(cmd.id),
        )
        if not payment:
            raise PaymentNotFound

        gateway = await self._factory.get(payment.method)

        if not payment.external_id:
            raise PaymentCheckForbidden

        invoice: Invoice = await gateway.get(
            data=GetInvoice(invoice_id=payment.external_id.value),
        )

        if invoice.status == InvoiceStatus.PAID:
            payment.confirm(now=self._clock.now())

            payment_dto = PaymentMapper.to_dto(src=payment)

            await self._session.commit()

            handler: (
                PaymentPurposeHandler | None
            ) = await self._handlers_registry.get(
                purpose_type=payment_dto.purpose.type,
            )
            if handler:
                await handler(payment=payment_dto)

            self._tasks.add(
                asyncio.create_task(
                    self._notification.send_admins(
                        request=NotificationRequest(
                            key="payment-confirmed-admin-notification"
                        ),
                        payment_id=payment_dto.id,
                        method=payment_dto.method,
                        amount=payment_dto.to_pay.amount,
                        currency=payment_dto.to_pay.currency,
                    )
                )
            )

        return invoice
