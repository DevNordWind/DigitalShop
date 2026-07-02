import logging
from copy import copy
from datetime import datetime

from app.app.common.exception import DataCorruptionError
from app.app.common.port.session import DatabaseSession
from app.app.common.port.telegram_notification import (
    Button,
    NotificationRequest,
    TelegramNotification,
)
from app.app.common.port.telegram_notification.dto import DEFAULT_BUTTON
from app.app.payment.dto.payment import PaymentDTO
from app.app.payment.port import PaymentPurposeHandler
from app.app.referral.cmd import (
    CreateReferralAwardFromOrder,
    CreateReferralAwardFromOrderCmd,
)
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
        create_award: CreateReferralAwardFromOrder,
        notification: TelegramNotification,
    ):
        self._position_repo = position_repo
        self._order_repo = order_repo
        self._redemption_repo = redemption_repo
        self._user_repo = user_repo
        self._fulfillment_service = fulfillment_service
        self._session = session
        self._clock = clock
        self._create_award = create_award
        self._notification = notification

    async def __call__(self, payment: PaymentDTO) -> None:
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
