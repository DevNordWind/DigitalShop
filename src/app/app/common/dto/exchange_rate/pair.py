from dataclasses import dataclass

from app.domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class CurrencyPairDTO:
    target: Currency
    source: Currency
