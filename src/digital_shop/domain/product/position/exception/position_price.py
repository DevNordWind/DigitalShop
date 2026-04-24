from dataclasses import dataclass

from domain.common.exception import ValueObjectError
from domain.common.money import Currency


class PositionPriceError(ValueObjectError): ...


@dataclass
class CurrencyMissingError(PositionPriceError):
    currency: Currency
