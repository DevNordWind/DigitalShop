from dataclasses import dataclass

from app.domain.common.money import Money
from app.domain.coupon.value_object import CouponId


@dataclass(frozen=True, slots=True)
class AppliedCoupon:
    coupon_id: CouponId
    discount: Money
