import logging
from datetime import datetime
from typing import override

from app.app.common.exception import DataCorruptionError
from app.app.common.port.session import DatabaseSession
from app.app.common.port.telegram_notification import (
    TelegramNotification,
)
from app.app.order.port import OrderNotifier, OrderReader
from app.app.payment.dto.payment import PaymentDTO
from app.app.payment.port import PaymentPurposeHandler
from app.app.referral.cmd import CreateReferralAwardFromOrder
from app.domain.common.port import Clock
from app.domain.coupon.entity import CouponRedemption
from app.domain.coupon.port import CouponRedemptionRepository
from app.domain.order.entity import Order
from app.domain.order.exception import OrderNotFoundError
from app.domain.order.port import OrderRepository
from app.domain.order.value_object import OrderId
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service.fulfillment import (
    PositionFulfillmentDomainService,
)
from app.domain.shopping.position.value_object import PositionId, SellContext
from app.domain.user.port import UserRepository

logger = logging.getLogger(__name__)


class ConfirmOrder(PaymentPurposeHandler):
    def __init__(
        self,
        position_repo: PositionRepository,
        order_repo: OrderRepository,
        redemption_repo: CouponRedemptionRepository,
        user_repo: UserRepository,
        fulfillment_service: PositionFulfillmentDomainService,
        session: DatabaseSession,
        clock: Clock,
        notification: TelegramNotification,
        order_reader: OrderReader,
        notifier: OrderNotifier,
        create_award: CreateReferralAwardFromOrder,
    ):
        self._position_repo = position_repo
        self._order_repo = order_repo
        self._redemption_repo = redemption_repo
        self._user_repo = user_repo
        self._fulfillment_service = fulfillment_service
        self._session = session
        self._clock = clock
        self._notification = notification
        self._order_reader = order_reader
        self._order_notifier = notifier
        self._create_award = create_award

    @override
    async def apply(self, payment: PaymentDTO) -> None:
        order: Order | None = await self._order_repo.acquire(
            order_id=OrderId(payment.purpose.reference_id),
        )
        if not order:
            raise OrderNotFoundError

        now: datetime = self._clock.now()

        order.confirm(now=now)

        if order.applied_coupon:
            redemption: (
                CouponRedemption | None
            ) = await self._redemption_repo.get_by_order_id(order_id=order.id)
            if not redemption:
                raise DataCorruptionError

            redemption.confirm(now=now)

        if order.items is None:
            raise DataCorruptionError

        position: Position | None = await self._position_repo.get(
            position_id=PositionId(order.position.position_id)
        )
        if position:
            await self._fulfillment_service.sell(
                position=position, snapshots=order.items, ctx=SellContext(now=now)
            )

        await self._create_award.apply(order=order)

    @override
    async def notify(self, payment: PaymentDTO) -> None:
        order = await self._order_reader.read_by_id(
            order_id=OrderId(payment.purpose.reference_id)
        )
        if order is None:
            raise DataCorruptionError

        await self._order_notifier.notify_confirmed(order=order)
        await self._create_award.notify(order=order)
