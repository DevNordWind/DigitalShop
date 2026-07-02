from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.coupon.dto.coupon import CouponDTO
from app.app.coupon.port import CouponReader
from app.domain.coupon.exception import CouponNotFoundError
from app.domain.coupon.service import CouponAccessService
from app.domain.coupon.value_object import CouponId


@dataclass(slots=True, frozen=True)
class GetCouponQuery:
    id: UUID


class GetCoupon:
    def __init__(self, reader: CouponReader, actor_provider: ActorProvider):
        self._reader = reader
        self._actor_provider = actor_provider

    async def __call__(self, query: GetCouponQuery) -> CouponDTO:
        CouponAccessService.ensure_can_view(actor=await self._actor_provider.get())

        coupon: CouponDTO | None = await self._reader.read(
            coupon_id=CouponId(query.id),
        )
        if coupon is None:
            raise CouponNotFoundError

        return coupon
