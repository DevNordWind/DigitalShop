from domain.common.exception import ValueObjectError


class CouponValidityError(ValueObjectError): ...


class CouponValidityExpired(CouponValidityError): ...
