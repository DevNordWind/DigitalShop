from app.domain.common.exception import (
    DomainConflictError,
    DomainError,
    DomainPermissionDeniedError,
    DomainRuleViolationError,
)


class PaymentCommissionRuleError(DomainError): ...


class PaymentCommissionRulePermissionDeniedError(
    PaymentCommissionRuleError, DomainPermissionDeniedError
): ...


class PaymentCommissionRuleAlreadyExistsError(
    PaymentCommissionRuleError, DomainConflictError
): ...


class CommissionCoefficientRequiredError(
    PaymentCommissionRuleError, DomainRuleViolationError
): ...
