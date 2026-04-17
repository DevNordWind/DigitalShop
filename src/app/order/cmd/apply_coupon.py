from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.common.port import DatabaseSession
from app.coupon.exception import CouponNotFound
from app.order.exception import OrderNotFound
from app.user.port import UserIdentifyProvider
from domain.common.port import Clock
from domain.coupon.entity import Coupon
from domain.coupon.port import CouponRedemptionRepository, CouponRepository
from domain.coupon.service import CouponRedemptionService
from domain.coupon.value_object import CouponCode
from domain.order.entity import Order
from domain.order.port.repository import OrderRepository
from domain.order.value_object import OrderId
from domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class ApplyCouponToOrderCmd:
    order_id: UUID
    coupon_code: str


class ApplyCouponToOrder:
    def __init__(
        self,
        order_repo: OrderRepository,
        redemption_repo: CouponRedemptionRepository,
        redemption_service: CouponRedemptionService,
        coupon_repo: CouponRepository,
        idp: UserIdentifyProvider,
        session: DatabaseSession,
        clock: Clock,
    ):
        self._order_repo: OrderRepository = order_repo
        self._redemption_repo: CouponRedemptionRepository = redemption_repo
        self._redemption_service: CouponRedemptionService = redemption_service
        self._coupon_repo: CouponRepository = coupon_repo
        self._idp: UserIdentifyProvider = idp
        self._clock: Clock = clock
        self._session: DatabaseSession = session

    async def __call__(self, cmd: ApplyCouponToOrderCmd) -> None:
        current_user_id: UserId = await self._idp.get_user_id()
        coupon_code = CouponCode(cmd.coupon_code)

        order: Order | None = await self._order_repo.get(
            order_id=OrderId(cmd.order_id),
        )
        if not order:
            raise OrderNotFound

        coupon: Coupon | None = await self._coupon_repo.get_by_code(
            code=coupon_code,
        )
        if not coupon:
            raise CouponNotFound

        now: datetime = self._clock.now()

        redemption = self._redemption_service.create(
            coupon_id=coupon.id,
            user_id=current_user_id,
            order_id=order.id,
            now=now,
        )
        await self._redemption_repo.add(redemption=redemption)

        order.apply_coupon(coupon=coupon, now=now)
        await self._session.commit()
