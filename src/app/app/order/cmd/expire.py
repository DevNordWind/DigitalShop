import logging
from copy import deepcopy
from datetime import datetime

from app.app.common.port.session import DatabaseSession
from app.app.common.port.telegram_notification import (
    NotificationRequest,
    TelegramNotification,
)
from app.app.payment.service import PaymentApplicationService
from app.app.payment.service.service import CancelPaymentData
from app.domain.common.port import Clock
from app.domain.order.const import ORDER_EXPIRATION_TIME
from app.domain.order.entity import Order
from app.domain.order.exception import OrderExpirationForbiddenError
from app.domain.order.port import OrderRepository
from app.domain.payment.port import PaymentRepository

logger = logging.getLogger(__name__)


class ExpireOutdatedOrders:
    def __init__(
        self,
        order_repo: OrderRepository,
        session: DatabaseSession,
        notification: TelegramNotification,
        payment_service: PaymentApplicationService,
        payment_repo: PaymentRepository,
        clock: Clock,
    ):
        self._order_repo = order_repo
        self._session = session
        self._notification = notification
        self._payment_service = payment_service
        self._clock = clock
        self._payment_repo = payment_repo

    async def __call__(self) -> None:
        now: datetime = self._clock.now()

        expired_orders: list[Order] = await self._order_repo.get_expired(
            now=now, ttl_seconds=ORDER_EXPIRATION_TIME
        )
        expired_orders_copy: list[Order] = deepcopy(expired_orders)

        for order in expired_orders:
            try:
                order.expire(now)
                if order.source and order.source.payment_id is not None:
                    await self._payment_service.cancel(
                        data=CancelPaymentData(id=order.source.payment_id.value)
                    )
            except OrderExpirationForbiddenError:
                logger.warning("Order %s cannot be expired", order.id)

        await self._session.commit()

        for order in expired_orders_copy:
            await self._notification.send(
                user_id=order.customer_id,
                request=NotificationRequest(key="order-expired-notification"),
                order_id=order.id.value,
            )
