from dataclasses import dataclass

from app.app.common.dto.query_params import OffsetPaginationParams
from app.app.common.port.actor_provider import ActorProvider
from app.app.coupon.dto.paginated import CouponsPaginated
from app.app.coupon.dto.sorting import CouponSortingParams
from app.app.coupon.port import CouponReader
from app.domain.common.port import Clock
from app.domain.coupon.enums import CouponStatus
from app.domain.coupon.service import CouponAccessService


@dataclass(slots=True, frozen=True)
class ListCouponsQuery:
    sorting: CouponSortingParams
    pagination: OffsetPaginationParams
    status: CouponStatus | None


class ListCoupons:
    def __init__(
        self,
        reader: CouponReader,
        actor_provider: ActorProvider,
        clock: Clock,
    ):
        self._reader = reader
        self._actor_provider = actor_provider
        self._clock = clock

    async def __call__(self, query: ListCouponsQuery) -> CouponsPaginated:
        CouponAccessService.ensure_can_view(actor=await self._actor_provider.get())

        return await self._reader.read_paginated(
            sorting=query.sorting,
            pagination=query.pagination,
            status=query.status,
            now=self._clock.now(),
        )
