from dataclasses import dataclass

from domain.common.exception import ValueObjectError
from domain.common.money import Currency


class ExchangeRateError(ValueObjectError): ...


class NegativeRateError(ExchangeRateError): ...


class ExchangeRateNotFound(ExchangeRateError): ...


@dataclass
class CurrencyMismatchError(ExchangeRateError):
    expected: Currency
    actual: Currency
