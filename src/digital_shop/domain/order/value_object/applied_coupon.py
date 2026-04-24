from dataclasses import dataclass

from domain.common.money import Money
from domain.coupon.value_object import CouponId


@dataclass(frozen=True, slots=True)
class AppliedCoupon:
    coupon_id: CouponId
    discount: Money
