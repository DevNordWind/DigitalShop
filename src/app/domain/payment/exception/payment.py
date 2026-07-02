from app.domain.common.exception import (
    DomainError,
    DomainPermissionDeniedError,
    DomainRuleViolationError,
    EntityNotFoundError,
)


class PaymentError(DomainError): ...


class PaymentNotFoundError(PaymentError, EntityNotFoundError): ...


class PaymentPermissionDeniedError(PaymentError, DomainPermissionDeniedError): ...


class PaymentStartForbiddenError(PaymentError, DomainRuleViolationError): ...


class PaymentCancellationForbiddenError(PaymentError, DomainRuleViolationError): ...


class PaymentCheckForbiddenError(PaymentError, DomainRuleViolationError): ...


class PaymentConfirmationForbiddenError(PaymentError, DomainRuleViolationError): ...


class PaymentFailureForbiddenError(PaymentError, DomainRuleViolationError): ...
