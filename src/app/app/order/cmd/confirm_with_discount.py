import logging
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.app.common.exception import DataCorruptionError
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.order.port import OrderReader
from app.app.referral.cmd import (
    CreateReferralAwardFromOrder,
)
from app.domain.common.port import Clock
from app.domain.coupon.entity import CouponRedemption
from app.domain.coupon.port import CouponRedemptionRepository
from app.domain.order.entity import Order
from app.domain.order.exception import OrderNotFoundError
from app.domain.order.port import OrderRepository
from app.domain.order.service import OrderAccessService
from app.domain.order.value_object import OrderId
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import (
    OutOfStockError,
    PositionNotFoundError,
)
from app.domain.shopping.position.item.value_object import ItemSnapshot
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service.fulfillment import (
    PositionFulfillmentDomainService,
)
from app.domain.shopping.position.value_object import (
    HoldContext,
    PositionId,
    SellContext,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class ConfirmOrderWithDiscountCmd:
    order_id: UUID


class ConfirmOrderWithDiscount:
    def __init__(
        self,
        position_repo: PositionRepository,
        order_repo: OrderRepository,
        order_reader: OrderReader,
        redemption_repo: CouponRedemptionRepository,
        fulfillment_service: PositionFulfillmentDomainService,
        session: DatabaseSession,
        actor_provider: ActorProvider,
        clock: Clock,
        create_award: CreateReferralAwardFromOrder,
    ):
        self._position_repo = position_repo
        self._order_repo = order_repo
        self._order_reader = order_reader
        self._redemption_repo = redemption_repo
        self._fulfillment_service = fulfillment_service
        self._session = session
        self._actor_provider = actor_provider
        self._clock: Clock = clock
        self._create_award = create_award

    async def __call__(self, cmd: ConfirmOrderWithDiscountCmd) -> None:
        order: Order | None = await self._order_repo.acquire(
            order_id=OrderId(cmd.order_id),
        )
        if not order:
            raise OrderNotFoundError

        OrderAccessService.ensure_can_checkout(
            actor=await self._actor_provider.get(), customer_id=order.customer_id
        )
        now: datetime = self._clock.now()

        position: Position | None = await self._position_repo.get(
            position_id=PositionId(order.position.position_id),
        )
        if not position:
            raise PositionNotFoundError

        try:
            items: tuple[ItemSnapshot, ...] = await self._fulfillment_service.hold(
                position=position, ctx=HoldContext(now=now, amount=order.items_amount)
            )
        except OutOfStockError:
            order.cancel(now)
            await self._session.commit()
            raise

        await self._fulfillment_service.sell(
            position=position, snapshots=items, ctx=SellContext(now=now)
        )
        order.confirm_with_discount(items=items, now=now)
        redemption: (
            CouponRedemption | None
        ) = await self._redemption_repo.get_by_order_id(order_id=order.id)
        if not redemption:
            raise DataCorruptionError

        redemption.confirm(now=now)
        await self._create_award.apply(order=order)
        order_id = order.id
        await self._session.commit()

        order_dto = await self._order_reader.read_by_id(order_id=order_id)
        if not order_dto:
            raise DataCorruptionError

        await self._create_award.notify(order=order_dto)
