from app.domain.common.exception import DomainRuleViolationError, ValueObjectError


class MoneyError(ValueObjectError): ...


class NegativeMoneyAmountError(MoneyError, DomainRuleViolationError): ...


class CurrencyDifferenceError(MoneyError, DomainRuleViolationError): ...
