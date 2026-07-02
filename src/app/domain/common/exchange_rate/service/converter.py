from collections.abc import Mapping, Sequence
from decimal import Decimal

from app.domain.common.exchange_rate import ExchangeRate, ExchangeRateNotFoundError
from app.domain.common.money import Currency, Money


class MoneyConverter:
    @classmethod
    def convert_many(
        cls,
        amounts: Mapping[Currency, Money],
        rates: Sequence[ExchangeRate],
        target: Currency,
    ) -> Money:
        if not amounts:
            return Money.zero(currency=target)

        total = Decimal("0.00")
        rate_map = {rate.pair.source: rate for rate in rates}

        for currency, money in amounts.items():
            if currency == target:
                total += money.amount
                continue
            try:
                total += rate_map[currency].convert(money).amount
            except KeyError as e:
                raise ExchangeRateNotFoundError from e

        return Money(currency=target, amount=total)
