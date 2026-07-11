from dataclasses import dataclass

from app.domain.common.exception import ValueObjectError


class CouponCodeError(ValueObjectError): ...


@dataclass
class CouponCodeTooLongError(CouponCodeError):
    max_length: int


@dataclass
class CouponCodeTooShortError(CouponCodeError):
    min_length: int
