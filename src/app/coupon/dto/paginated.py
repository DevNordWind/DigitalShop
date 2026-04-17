from dataclasses import dataclass

from app.coupon.dto.coupon import CouponDTO


@dataclass(slots=True, frozen=True)
class CouponsPaginated:
    coupons: list[CouponDTO]
    total: int
