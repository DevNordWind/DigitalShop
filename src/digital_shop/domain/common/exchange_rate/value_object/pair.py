from dataclasses import dataclass

from domain.common.exchange_rate.exception.pair import CurrencyPairSameCurrency
from domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class CurrencyPair:
    target: Currency
    source: Currency

    def __post_init__(self) -> None:
        if self.target == self.source:
            raise CurrencyPairSameCurrency
