from dataclasses import dataclass
from uuid import UUID

from app.coupon.dto.coupon import CouponDTO
from app.coupon.exception import CouponNotFound
from app.coupon.port import CouponReader
from app.user.port import UserIdentifyProvider
from domain.coupon.exception import CouponPermissionDenied
from domain.coupon.service.access_service import CouponAccessService
from domain.coupon.value_object import CouponId


@dataclass(slots=True, frozen=True)
class GetCouponQuery:
    id: UUID


class GetCoupon:
    def __init__(self, reader: CouponReader, idp: UserIdentifyProvider):
        self._reader: CouponReader = reader
        self._idp: UserIdentifyProvider = idp

    async def __call__(self, query: GetCouponQuery) -> CouponDTO:
        if not CouponAccessService.can_view(
            viewer_role=await self._idp.get_role(),
        ):
            raise CouponPermissionDenied

        coupon: CouponDTO | None = await self._reader.read(
            coupon_id=CouponId(query.id),
        )
        if coupon is None:
            raise CouponNotFound

        return coupon
