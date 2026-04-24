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
    PaymentPurposeHandler,
    PaymentPurposeHandlersRegistry,
)
from domain.common.port import Clock
from domain.payment.entity import Payment
from domain.payment.port import PaymentRepository
from domain.payment.value_object import PaymentId


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
    ):
        self._repo: PaymentRepository = repo
        self._session: DatabaseSession = session
        self._clock: Clock = clock
        self._handlers_registry: PaymentPurposeHandlersRegistry = (
            handlers_registry
        )
        self._notification: TelegramNotification = notification
        self._tasks: set[Task[Any]] = set()

    async def __call__(self, cmd: ConfirmPaymentCmd) -> None:
        payment: Payment | None = await self._repo.get(
            payment_id=PaymentId(cmd.id),
        )
        if not payment:
            raise PaymentNotFound

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
