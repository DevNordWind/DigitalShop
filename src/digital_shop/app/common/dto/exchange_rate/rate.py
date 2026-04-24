from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.common.dto.exchange_rate.pair import CurrencyPairDTO


@dataclass(slots=True, frozen=True)
class ExchangeRateDTO:
    pair: CurrencyPairDTO
    rate: Decimal
    timestamp: datetime
