from dataclasses import dataclass

from app.common.dto.query_params import OffsetPaginationParams
from app.coupon.dto.paginated import CouponsPaginated
from app.coupon.dto.sorting import CouponSortingParams
from app.coupon.port import CouponReader
from app.user.port import UserIdentifyProvider
from domain.common.port import Clock
from domain.coupon.enums import CouponStatus
from domain.coupon.exception import CouponPermissionDenied
from domain.coupon.service.access_service import CouponAccessService


@dataclass(slots=True, frozen=True)
class ListCouponsQuery:
    sorting: CouponSortingParams
    pagination: OffsetPaginationParams
    status: CouponStatus | None


class ListCoupons:
    def __init__(
        self,
        reader: CouponReader,
        idp: UserIdentifyProvider,
        clock: Clock,
    ):
        self._reader: CouponReader = reader
        self._idp: UserIdentifyProvider = idp
        self._clock: Clock = clock

    async def __call__(self, query: ListCouponsQuery) -> CouponsPaginated:
        if not CouponAccessService.can_view(
            viewer_role=await self._idp.get_role(),
        ):
            raise CouponPermissionDenied

        return await self._reader.read_paginated(
            sorting=query.sorting,
            pagination=query.pagination,
            status=query.status,
            now=self._clock.now(),
        )
