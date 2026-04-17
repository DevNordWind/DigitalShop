from dataclasses import dataclass
from datetime import datetime

from domain.common.money import Money
from domain.coupon.enums import CouponStatus
from domain.coupon.exception import (
    CouponAlreadyRevoked,
    CouponExpired,
    CouponNotStarted,
    CouponRevoked,
)
from domain.coupon.strategy import DiscountStrategy
from domain.coupon.value_object import CouponCode, CouponId, CouponValidity
from domain.user.value_object import UserId


@dataclass
class Coupon:
    id: CouponId
    creator_id: UserId

    code: CouponCode
    discount: DiscountStrategy

    valid_from: CouponValidity
    valid_until: CouponValidity | None

    created_at: datetime

    is_revoked: bool = False

    def calculate_discount(self, now: datetime, sub_total: Money) -> Money:
        self.ensure_can_be_used(now)
        return self.discount.calculate(sub_total)

    def calculate_status(self, now: datetime) -> CouponStatus:
        if self.is_revoked:
            return CouponStatus.REVOKED

        if now < self.valid_from.value:
            return CouponStatus.NOT_STARTED

        if self.valid_until and now > self.valid_until.value:
            return CouponStatus.EXPIRED

        return CouponStatus.ACTIVE

    def ensure_can_be_used(self, now: datetime) -> None:
        match self.calculate_status(now):
            case CouponStatus.REVOKED:
                raise CouponRevoked
            case CouponStatus.NOT_STARTED:
                raise CouponNotStarted
            case CouponStatus.EXPIRED:
                raise CouponExpired
            case CouponStatus.ACTIVE:
                pass

    def revoke(self) -> None:
        if self.is_revoked:
            raise CouponAlreadyRevoked

        self.is_revoked = True
