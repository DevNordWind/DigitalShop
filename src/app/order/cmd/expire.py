import logging
from copy import deepcopy
from datetime import datetime

from app.common.exception import DataCorruptionError
from app.common.port import DatabaseSession, TelegramNotification
from app.common.port.telegram_notification import NotificationRequest
from app.payment.port import (
    PaymentMethodGateway,
    PaymentMethodGatewayError,
    PaymentMethodGatewayFactory,
)
from app.payment.port.payment import CancelInvoice
from domain.common.port import Clock
from domain.order.entity import ORDER_TTL_SECONDS, Order
from domain.order.exception import OrderExpirationForbidden
from domain.order.port.repository import OrderRepository
from domain.payment.entity import Payment
from domain.payment.port import PaymentRepository

logger = logging.getLogger(__name__)


class ExpireOutdatedOrders:
    def __init__(
        self,
        order_repo: OrderRepository,
        session: DatabaseSession,
        notification: TelegramNotification,
        payment_factory: PaymentMethodGatewayFactory,
        payment_repo: PaymentRepository,
        clock: Clock,
    ):
        self._order_repo = order_repo
        self._session = session
        self._notification = notification
        self._clock = clock
        self._payment_repo = payment_repo
        self._payment_factory: PaymentMethodGatewayFactory = payment_factory

    async def __call__(self) -> None:
        now: datetime = self._clock.now()

        expired_orders: list[Order] = await self._order_repo.get_expired(
            now=now, ttl_seconds=ORDER_TTL_SECONDS
        )
        expired_orders_copy: list[Order] = deepcopy(expired_orders)

        for order in expired_orders:
            try:
                order.expire(now)
                if order.source and order.source.payment_id is not None:
                    payment: Payment | None = await self._payment_repo.get(
                        payment_id=order.source.payment_id
                    )
                    if not payment:
                        raise DataCorruptionError(
                            f"Order {order.id} exists but it's payment was not found",  # noqa: E501
                        )
                    payment.cancel(now)
                    if payment.external_id:
                        gateway: PaymentMethodGateway = (
                            await self._payment_factory.get(
                                method=payment.method
                            )
                        )
                        try:
                            await gateway.cancel(
                                data=CancelInvoice(
                                    invoice_id=payment.external_id.value,
                                ),
                            )
                        except PaymentMethodGatewayError as e:
                            logger.error(e)

            except OrderExpirationForbidden:
                logger.warning("Order %s cannot be expired", order.id)

        await self._session.commit()

        for order in expired_orders_copy:
            await self._notification.send(
                user_id=order.customer_id,
                request=NotificationRequest(key="order-expired-notification"),
                order_id=order.id.value,
            )
