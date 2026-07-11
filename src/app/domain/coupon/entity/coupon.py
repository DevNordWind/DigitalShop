from dataclasses import dataclass
from datetime import datetime

from app.domain.common.money import Money
from app.domain.coupon.enums import CouponStatus
from app.domain.coupon.exception import (
    CouponAlreadyRevokedError,
    CouponExpiredError,
    CouponNotStartedError,
    CouponRevokedError,
)
from app.domain.coupon.strategy import DiscountStrategy
from app.domain.coupon.value_object import CouponCode, CouponId, CouponValidity
from app.domain.user.value_object import UserId


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
        match self.calculate_status(now):
            case CouponStatus.REVOKED:
                raise CouponRevokedError
            case CouponStatus.NOT_STARTED:
                raise CouponNotStartedError
            case CouponStatus.EXPIRED:
                raise CouponExpiredError
            case CouponStatus.ACTIVE:
                pass

        return self.discount.calculate(sub_total)

    def calculate_status(self, now: datetime) -> CouponStatus:
        if self.is_revoked:
            return CouponStatus.REVOKED

        if now < self.valid_from.value:
            return CouponStatus.NOT_STARTED

        if self.valid_until and now > self.valid_until.value:
            return CouponStatus.EXPIRED

        return CouponStatus.ACTIVE

    def revoke(self) -> None:
        if self.is_revoked:
            raise CouponAlreadyRevokedError

        self.is_revoked = True
