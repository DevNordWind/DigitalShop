from dataclasses import dataclass
from typing import Final

from domain.coupon.exception import CouponCodeTooLong, CouponCodeTooShort

COUPON_CODE_MIN_LENGTH: Final[int] = 2
COUPON_CODE_MAX_LENGTH: Final[int] = 64


@dataclass(slots=True, frozen=True)
class CouponCode:
    value: str

    def __post_init__(self) -> None:
        length: int = len(self.value)

        if length < COUPON_CODE_MIN_LENGTH:
            raise CouponCodeTooShort(min_length=COUPON_CODE_MIN_LENGTH)

        if length > COUPON_CODE_MAX_LENGTH:
            raise CouponCodeTooLong(max_length=COUPON_CODE_MAX_LENGTH)
