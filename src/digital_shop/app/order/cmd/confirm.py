import logging
from copy import copy
from datetime import datetime

from app.common.exception import DataCorruptionError
from app.common.port import DatabaseSession, TelegramNotification
from app.common.port.telegram_notification import Button, NotificationRequest
from app.common.port.telegram_notification.dto import DEFAULT_BUTTON
from app.order.exception import OrderNotFound
from app.payment.dto.payment import PaymentDTO
from app.payment.port import PaymentPurposeHandler
from app.referral.cmd import (
    CreateReferralAwardFromOrder,
    CreateReferralAwardFromOrderCmd,
)
from domain.common.port import Clock
from domain.coupon.entity import CouponRedemption
from domain.coupon.port import CouponRedemptionRepository
from domain.order.entity import Order
from domain.order.port.repository import OrderRepository
from domain.order.value_object import OrderId
from domain.product.position.item.value_object import ItemId
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionWarehouseService
from domain.user.port import UserRepository

logger = logging.getLogger(__name__)


class ConfirmOrder(PaymentPurposeHandler):
    def __init__(
        self,
        position_repo: PositionRepository,
        order_repo: OrderRepository,
        redemption_repo: CouponRedemptionRepository,
        user_repo: UserRepository,
        warehouse_service: PositionWarehouseService,
        session: DatabaseSession,
        clock: Clock,
        create_award: CreateReferralAwardFromOrder,
        notification: TelegramNotification,
    ):
        self._position_repo: PositionRepository = position_repo
        self._order_repo: OrderRepository = order_repo
        self._redemption_repo: CouponRedemptionRepository = redemption_repo
        self._user_repo: UserRepository = user_repo
        self._warehouse_service: PositionWarehouseService = warehouse_service
        self._session: DatabaseSession = session
        self._clock: Clock = clock
        self._create_award: CreateReferralAwardFromOrder = create_award
        self._notification: TelegramNotification = notification

    async def __call__(self, payment: PaymentDTO) -> None:
        order: Order | None = await self._order_repo.get(
            order_id=OrderId(payment.purpose.reference_id),
        )
        if not order:
            raise OrderNotFound

        now: datetime = self._clock.now()

        order.confirm(now=now)

        if order.applied_coupon:
            redemption: (
                CouponRedemption | None
            ) = await self._redemption_repo.get_by_order_id(order_id=order.id)
            if not redemption:
                raise DataCorruptionError

            redemption.confirm(now=now)

        if order.items is not None:
            items_ids: set[ItemId] = {
                ItemId(item.item_id) for item in order.items
            }

            await self._warehouse_service.sell_reserved(
                items_ids=list(items_ids),
                now=now,
            )

        order_copy: Order = copy(order)

        await self._session.commit()

        await self._notification.send(
            user_id=order_copy.customer_id,
            request=NotificationRequest(
                key="order-confirmed-notification",
                buttons=[
                    Button(
                        key="order-confirmed-notification.to-order-btn",
                        data=f"to_order:{order_copy.id.value}",
                    ),
                    DEFAULT_BUTTON,
                ],
            ),
            order_id=order_copy.id.value,
            amount=order_copy.total.amount,
            currency=order_copy.total.currency,
        )
        try:
            await self._create_award(
                CreateReferralAwardFromOrderCmd(
                    order_id=payment.purpose.reference_id,
                ),
            )
        except Exception as e:
            logger.error(e)
