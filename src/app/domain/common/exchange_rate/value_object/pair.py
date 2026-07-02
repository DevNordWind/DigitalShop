from dataclasses import dataclass

from app.domain.common.exchange_rate.exception.pair import (
    CurrencyPairSameCurrencyError,
)
from app.domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class CurrencyPair:
    target: Currency
    source: Currency

    def __post_init__(self) -> None:
        if self.target == self.source:
            raise CurrencyPairSameCurrencyError
