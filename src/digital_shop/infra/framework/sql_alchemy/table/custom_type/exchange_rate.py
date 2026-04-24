from decimal import Decimal
from typing import Any

from domain.common.exchange_rate import CurrencyPair, ExchangeRate
from domain.common.money import Currency
from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB


class ExchangeRateType(TypeDecorator[ExchangeRate]):
    impl = JSONB
    cache_ok = True

    def process_bind_param(
        self,
        value: ExchangeRate | None,
        dialect: Dialect,
    ) -> dict[str, Any] | None:
        if value is None:
            return None

        return {
            "source_currency": value.pair.source,
            "target_currency": value.pair.target,
            "rate": str(value.rate),
            "timestamp": value.timestamp,
        }

    def process_result_value(
        self,
        value: dict[str, Any] | None,
        dialect: Dialect,
    ) -> ExchangeRate | None:
        if value is None:
            return None

        return ExchangeRate(
            pair=CurrencyPair(
                source=Currency(value["source_currency"]),
                target=Currency("target_currency"),
            ),
            rate=Decimal(value["rate"]),
            timestamp=value["timestamp"],
        )
