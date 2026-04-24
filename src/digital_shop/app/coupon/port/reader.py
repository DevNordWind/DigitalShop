from abc import ABC, abstractmethod
from datetime import datetime

from app.common.dto.query_params import OffsetPaginationParams
from app.coupon.dto.coupon import CouponDTO
from app.coupon.dto.paginated import CouponsPaginated
from app.coupon.dto.sorting import CouponSortingParams
from domain.coupon.enums import CouponStatus
from domain.coupon.value_object import CouponId


class CouponReader(ABC):
    @abstractmethod
    async def read(self, coupon_id: CouponId) -> CouponDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def read_paginated(
        self,
        sorting: CouponSortingParams,
        pagination: OffsetPaginationParams,
        status: CouponStatus | None,
        now: datetime,
    ) -> CouponsPaginated:
        raise NotImplementedError
