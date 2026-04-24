from dataclasses import dataclass
from decimal import Decimal

from domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class MoneyDTO:
    amount: Decimal
    currency: Currency
