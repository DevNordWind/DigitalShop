from app.domain.common.exception import DomainError, DomainRuleViolationError


class CouponRedemptionError(DomainError): ...


class CouponRedemptionCancellationForbiddenError(
    CouponRedemptionError, DomainRuleViolationError
): ...


class CouponRedemptionConfirmationForbiddenError(
    CouponRedemptionError, DomainRuleViolationError
): ...
