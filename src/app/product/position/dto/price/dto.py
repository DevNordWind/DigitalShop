from dataclasses import dataclass

from app.common.dto.money import MoneyDTO
from domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class PositionPriceDTO:
    base_currency: Currency
    prices: dict[Currency, MoneyDTO]

    def get(self, currency: Currency) -> MoneyDTO:
        return self.prices[currency]
