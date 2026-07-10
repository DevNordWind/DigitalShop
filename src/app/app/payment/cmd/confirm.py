from dataclasses import dataclass
from uuid import UUID

from app.app.common.background import BackgroundTasks
from app.app.common.port.session import DatabaseSession
from app.app.common.port.telegram_notification import (
    NotificationRequest,
    TelegramNotification,
)
from app.app.payment.dto.payment import PaymentMapper
from app.app.payment.port import PaymentPurposeHandler, PaymentPurposeHandlersRegistry
from app.domain.common.port import Clock
from app.domain.payment.entity import Payment
from app.domain.payment.exception import PaymentNotFoundError
from app.domain.payment.port import PaymentRepository
from app.domain.payment.value_object import PaymentId


@dataclass(slots=True, frozen=True)
class ConfirmPaymentCmd:
    id: UUID


class ConfirmPayment:
    def __init__(
        self,
        repo: PaymentRepository,
        session: DatabaseSession,
        clock: Clock,
        handlers_registry: PaymentPurposeHandlersRegistry,
        notification: TelegramNotification,
        background: BackgroundTasks,
    ):
        self._repo = repo
        self._session = session
        self._clock = clock
        self._handlers_registry = handlers_registry
        self._notification = notification
        self._background = background

    async def __call__(self, cmd: ConfirmPaymentCmd) -> None:
        payment: Payment | None = await self._repo.acquire(
            payment_id=PaymentId(cmd.id),
        )
        if not payment:
            raise PaymentNotFoundError

        payment.confirm(now=self._clock.now())

        payment_dto = PaymentMapper.to_dto(src=payment)

        handler: PaymentPurposeHandler = await self._handlers_registry.get(
            purpose_type=payment_dto.purpose.type,
        )
        await handler.apply(payment=payment_dto)

        await self._session.commit()
        await handler.notify(payment=payment_dto)

        self._background.spawn(
            self._notification.send_admins(
                request=NotificationRequest(key="payment-confirmed-admin-notification"),
                payment_id=payment_dto.id,
                method=payment_dto.method,
                amount=payment_dto.to_pay.amount,
                currency=payment_dto.to_pay.currency,
            )
        )
