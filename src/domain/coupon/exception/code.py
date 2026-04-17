from dataclasses import dataclass

from domain.common.exception import ValueObjectError


class CouponCodeError(ValueObjectError): ...


@dataclass
class CouponCodeTooLong(CouponCodeError):
    max_length: int


@dataclass
class CouponCodeTooShort(CouponCodeError):
    min_length: int
