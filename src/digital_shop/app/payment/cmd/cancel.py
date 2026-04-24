from contextlib import suppress
from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.payment.exception import PaymentNotFound
from app.payment.port import (
    PaymentMethodGatewayError,
    PaymentMethodGatewayFactory,
)
from app.payment.port.payment import CancelInvoice
from domain.common.port import Clock
from domain.payment.entity import Payment
from domain.payment.port import PaymentRepository
from domain.payment.value_object import PaymentId


@dataclass(slots=True, frozen=True)
class CancelPaymentCmd:
    id: UUID


class CancelPayment:
    def __init__(
        self,
        repo: PaymentRepository,
        session: DatabaseSession,
        clock: Clock,
        factory: PaymentMethodGatewayFactory,
    ):
        self._repo: PaymentRepository = repo
        self._session: DatabaseSession = session
        self._clock: Clock = clock
        self._factory: PaymentMethodGatewayFactory = factory

    async def __call__(self, cmd: CancelPaymentCmd) -> None:
        payment: Payment | None = await self._repo.get(
            payment_id=PaymentId(cmd.id),
        )
        if not payment:
            raise PaymentNotFound

        payment.cancel(now=self._clock.now())

        gateway = await self._factory.get(payment.method)

        with suppress(PaymentMethodGatewayError):
            if payment.external_id:
                await gateway.cancel(
                    data=CancelInvoice(invoice_id=payment.external_id.value),
                )

        await self._session.commit()
