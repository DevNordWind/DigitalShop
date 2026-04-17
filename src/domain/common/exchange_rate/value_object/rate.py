from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.common.exchange_rate import (
    CurrencyMismatchError,
    NegativeRateError,
)
from domain.common.exchange_rate.value_object.pair import CurrencyPair
from domain.common.money import Money


@dataclass(slots=True, frozen=True)
class ExchangeRate:
    pair: CurrencyPair
    rate: Decimal
    timestamp: datetime

    def __post_init__(self) -> None:
        if self.rate < Decimal("0.00"):
            raise NegativeRateError

    def convert(self, amount: Money) -> Money:
        if amount.currency != self.pair.source:
            raise CurrencyMismatchError(
                expected=self.pair.source,
                actual=amount.currency,
            )

        return Money(
            currency=self.pair.target,
            amount=self.rate * amount.amount,
        )
