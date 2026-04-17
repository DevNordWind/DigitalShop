from dataclasses import dataclass
from datetime import datetime

from app.common.port import DatabaseSession
from app.coupon.dto.discount import DiscountDTO, DiscountMapper
from app.user.service import GetCurrentUser
from domain.coupon.port import CouponRepository
from domain.coupon.service.service import CouponService
from domain.coupon.value_object import CouponCode, CouponId
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class CreateCouponCmd:
    code: str
    discount: DiscountDTO
    valid_from: datetime | None
    valid_until: datetime | None


class CreateCoupon:
    def __init__(
        self,
        repository: CouponRepository,
        session: DatabaseSession,
        service: CouponService,
        current_user: GetCurrentUser,
    ):
        self._repository: CouponRepository = repository
        self._session: DatabaseSession = session
        self._service: CouponService = service
        self._current_user: GetCurrentUser = current_user

    async def __call__(self, cmd: CreateCouponCmd) -> CouponId:
        creator: User = await self._current_user()

        coupon = self._service.create(
            creator=creator,
            code=CouponCode(cmd.code),
            discount=DiscountMapper.to_strategy(src=cmd.discount),
            valid_from=cmd.valid_from,
            valid_until=cmd.valid_until,
        )
        coupon_id: CouponId = coupon.id
        await self._repository.add(coupon=coupon)

        await self._session.commit()

        return coupon_id
