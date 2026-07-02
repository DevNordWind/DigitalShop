from dataclasses import dataclass

from app.domain.common.exception import ValueObjectError
from app.domain.common.money import Currency


class ExchangeRateError(ValueObjectError): ...


class NegativeRateError(ExchangeRateError): ...


class ExchangeRateNotFoundError(ExchangeRateError): ...


@dataclass
class CurrencyMismatchError(ExchangeRateError):
    expected: Currency
    actual: Currency
