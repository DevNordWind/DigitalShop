from app.domain.common.exception import ValueObjectError


class CouponValidityError(ValueObjectError): ...


class CouponValidityCannotBeInPastError(CouponValidityError): ...
