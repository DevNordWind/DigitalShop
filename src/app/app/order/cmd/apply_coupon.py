from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.actor import UserActor
from app.domain.common.port import Clock
from app.domain.coupon.entity import Coupon
from app.domain.coupon.exception import CouponNotFoundError
from app.domain.coupon.port import CouponRedemptionRepository, CouponRepository
from app.domain.coupon.service import CouponRedemptionDomainService
from app.domain.coupon.value_object import CouponCode
from app.domain.order.entity import Order
from app.domain.order.exception import OrderNotFoundError
from app.domain.order.port import OrderRepository
from app.domain.order.service import OrderAccessService
from app.domain.order.value_object import OrderId


@dataclass(slots=True, frozen=True)
class ApplyCouponToOrderCmd:
    order_id: UUID
    coupon_code: str


class ApplyCouponToOrder:
    def __init__(
        self,
        order_repo: OrderRepository,
        redemption_repo: CouponRedemptionRepository,
        redemption_service: CouponRedemptionDomainService,
        coupon_repo: CouponRepository,
        actor_provider: ActorProvider,
        session: DatabaseSession,
        clock: Clock,
    ):
        self._order_repo = order_repo
        self._redemption_repo = redemption_repo
        self._redemption_service = redemption_service
        self._coupon_repo = coupon_repo
        self._actor_provider = actor_provider
        self._clock = clock
        self._session = session

    async def __call__(self, cmd: ApplyCouponToOrderCmd) -> None:
        coupon_code = CouponCode(cmd.coupon_code)
        order: Order | None = await self._order_repo.get(
            order_id=OrderId(cmd.order_id),
        )
        if not order:
            raise OrderNotFoundError

        actor: UserActor = OrderAccessService.ensure_can_apply_coupon(
            actor=await self._actor_provider.get(), customer_id=order.customer_id
        )
        coupon: Coupon | None = await self._coupon_repo.get_by_code(
            code=coupon_code,
        )
        if not coupon:
            raise CouponNotFoundError

        now: datetime = self._clock.now()

        redemption = self._redemption_service.create(
            coupon_id=coupon.id,
            user_id=actor.id,
            order_id=order.id,
            now=now,
        )
        await self._redemption_repo.add(redemption=redemption)

        order.apply_coupon(coupon=coupon, now=now)
        await self._session.commit()
