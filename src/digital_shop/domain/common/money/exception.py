from domain.common.exception import ValueObjectError


class MoneyError(ValueObjectError): ...


class NegativeMoneyAmount(MoneyError): ...


class CurrencyDifferenceError(MoneyError): ...
