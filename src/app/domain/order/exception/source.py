from app.domain.common.exception import (
    DomainRuleViolationError,
    ValueObjectError,
)


class PaymentSourceError(ValueObjectError): ...


class PaymentIdRequiredError(PaymentSourceError, DomainRuleViolationError): ...
