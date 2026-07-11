from dataclasses import dataclass
from typing import Final

from app.domain.coupon.exception import (
    CouponCodeTooLongError,
    CouponCodeTooShortError,
)

COUPON_CODE_MIN_LENGTH: Final[int] = 2
COUPON_CODE_MAX_LENGTH: Final[int] = 64


@dataclass(slots=True, frozen=True)
class CouponCode:
    value: str

    def __post_init__(self) -> None:
        normalized: str = self.value.strip()
        length: int = len(normalized)

        if length < COUPON_CODE_MIN_LENGTH:
            raise CouponCodeTooShortError(min_length=COUPON_CODE_MIN_LENGTH)

        if length > COUPON_CODE_MAX_LENGTH:
            raise CouponCodeTooLongError(max_length=COUPON_CODE_MAX_LENGTH)

        object.__setattr__(self, "value", normalized)
