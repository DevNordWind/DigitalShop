from app.domain.common.exception import (
    DomainError,
    DomainPermissionDeniedError,
    DomainRuleViolationError,
    EntityNotFoundError,
)


class OrderError(DomainError): ...


class OrderNotFoundError(OrderError, EntityNotFoundError): ...


class OrderCouponApplicationForbiddenError(OrderError, DomainRuleViolationError): ...


class OrderCancellationForbiddenError(OrderError, DomainRuleViolationError): ...


class OrderPermissionDeniedError(OrderError, DomainPermissionDeniedError): ...


class OrderFailureForbiddenError(OrderError, DomainRuleViolationError): ...


class OrderExpirationForbiddenError(OrderError, DomainRuleViolationError): ...


class OrderConfirmationForbiddenError(OrderError, DomainRuleViolationError): ...


class OrderAwaitingPaymentForbiddenError(OrderError, DomainRuleViolationError): ...


class OrderCurrencyChangeForbiddenError(OrderError, DomainRuleViolationError): ...


class OrderItemsAmountChangeForbiddenError(OrderError, DomainRuleViolationError): ...


class OrderFreePaymentForbiddenError(OrderError, DomainRuleViolationError): ...


class OrderPaymentRequiredError(OrderError, DomainRuleViolationError): ...


class OrderAppliedCouponRequiredError(OrderError, DomainRuleViolationError): ...
