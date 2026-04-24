from dataclasses import dataclass
from datetime import datetime, timedelta

from domain.common.exchange_rate import CurrencyPair, ExchangeRate


@dataclass(slots=True, frozen=True)
class CachedExchangeRates:
    rates: dict[CurrencyPair, ExchangeRate]
    received_at: datetime

    def is_expired(self, ttl: timedelta, now: datetime) -> bool:
        return now > self.received_at + ttl
