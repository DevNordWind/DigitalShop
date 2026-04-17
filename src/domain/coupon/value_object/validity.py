from dataclasses import dataclass
from datetime import datetime

from domain.coupon.exception import (
    CouponValidityExpired,
)


@dataclass(slots=True, frozen=True)
class CouponValidity:
    value: datetime

    @classmethod
    def create(cls, now: datetime, value: datetime) -> CouponValidity:
        if value < now:
            raise CouponValidityExpired

        return CouponValidity(value=value)
