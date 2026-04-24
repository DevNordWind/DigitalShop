from dataclasses import dataclass, field
from typing import Final
from uuid import UUID

from app.common.dto.query_params import SortingOrder
from app.coupon.dto.sorting import CouponSortingParams
from domain.coupon.enums import CouponStatus

CTX_KEY: Final[str] = "CTX_KEY"

COUPONS_SCROLL: Final[str] = "COUPONS_SCROLL"
COUPONS_HEIGHT: Final[int] = 8


@dataclass(slots=True)
class AdminCouponCtx:
    sorting: CouponSortingParams = field(
        default=CouponSortingParams(
            field="created_at",
            order=SortingOrder.DESC,
        ),
    )
    status: CouponStatus | None = None

    current_coupon_id: UUID | None = None
