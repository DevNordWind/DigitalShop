from app.domain.common.exception import (
    DomainConflictError,
    DomainError,
    DomainPermissionDeniedError,
    DomainRuleViolationError,
    EntityNotFoundError,
)


class CouponError(DomainError): ...


class CouponNotFoundError(CouponError, EntityNotFoundError): ...


class CouponPermissionDeniedError(CouponError, DomainPermissionDeniedError): ...


class CouponAlreadyExistsError(CouponError, DomainConflictError): ...


class CouponAlreadyRevokedError(CouponError, DomainConflictError): ...


class CouponDiscountUnsupportedCurrencyError(CouponError, DomainRuleViolationError): ...


class CouponUseForbiddenError(CouponError): ...


class CouponAlreadyUsedByUserError(CouponUseForbiddenError, DomainConflictError): ...


class CouponRevokedError(CouponUseForbiddenError, DomainRuleViolationError): ...


class CouponNotStartedError(CouponUseForbiddenError, DomainRuleViolationError): ...


class CouponExpiredError(CouponUseForbiddenError, DomainRuleViolationError): ...
