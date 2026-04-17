from dataclasses import dataclass

from frozendict import frozendict

from domain.common.money import Currency, Money
from domain.product.position.exception import (
    CurrencyMissingError,
)


@dataclass(slots=True, frozen=True)
class PositionPrice:
    base_currency: Currency
    prices: frozendict[Currency, Money]

    def __post_init__(self) -> None:
        missing = set(Currency) - self.prices.keys()
        if missing:
            raise CurrencyMissingError(currency=next(iter(missing)))

    def get_default(self) -> Money:
        return self.prices[self.base_currency]

    def get(self, currency: Currency) -> Money:
        return self.prices[currency]

    def set(self, price: Money) -> PositionPrice:
        return PositionPrice(
            base_currency=self.base_currency,
            prices=frozendict(self.prices | {price.currency: price}),
        )

    def change_base_currency(self, currency: Currency) -> PositionPrice:
        return PositionPrice(base_currency=currency, prices=self.prices)
