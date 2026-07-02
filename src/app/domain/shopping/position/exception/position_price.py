from dataclasses import dataclass

from app.domain.common.exception import ValueObjectError
from app.domain.common.money import Currency


class PositionPriceError(ValueObjectError): ...


@dataclass
class CurrencyMissingError(PositionPriceError):
    currency: Currency
