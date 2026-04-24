from decimal import Decimal
from typing import Any

from domain.common.money import Currency, Money
from domain.product.position.value_object import PositionPrice
from frozendict import frozendict
from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB


class PositionPriceType(TypeDecorator[PositionPrice]):
    impl = JSONB
    cache_ok = True

    def process_bind_param(
        self,
        value: PositionPrice | None,
        dialect: Dialect,
    ) -> dict[str, Any] | None:
        if value is None:
            return None

        return {
            "base_currency": value.base_currency.value,
            "prices": {
                currency.value: {
                    "amount": str(money.amount),
                    "currency": money.currency.value,
                }
                for currency, money in value.prices.items()
            },
        }

    def process_result_value(
        self,
        value: dict[str, Any] | None,
        dialect: Dialect,
    ) -> PositionPrice | None:
        if value is None:
            return None

        mapping: dict[Currency, Money] = {}
        for currency_raw, money_raw in value["prices"].items():
            currency = Currency(currency_raw)
            mapping[currency] = Money(
                amount=Decimal(money_raw["amount"]),
                currency=currency,
            )

        return PositionPrice(
            base_currency=Currency(value["base_currency"]),
            prices=frozendict(mapping),
        )
