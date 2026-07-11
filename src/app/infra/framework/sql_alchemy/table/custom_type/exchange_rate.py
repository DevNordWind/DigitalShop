from decimal import Decimal
from typing import Any, override

from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB

from app.domain.common.exchange_rate import CurrencyPair, ExchangeRate
from app.domain.common.money import Currency


class ExchangeRateType(TypeDecorator[ExchangeRate]):
    impl = JSONB
    cache_ok = True

    @override
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

    @override
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
                target=Currency(value["target_currency"]),
            ),
            rate=Decimal(value["rate"]),
            timestamp=value["timestamp"],
        )
