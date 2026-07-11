from dataclasses import dataclass
from datetime import datetime

from app.domain.coupon.exception import (
    CouponValidityCannotBeInPastError,
)


@dataclass(slots=True, frozen=True)
class CouponValidity:
    value: datetime

    @classmethod
    def create(cls, now: datetime, value: datetime) -> CouponValidity:
        if value < now:
            raise CouponValidityCannotBeInPastError

        return CouponValidity(value=value)
