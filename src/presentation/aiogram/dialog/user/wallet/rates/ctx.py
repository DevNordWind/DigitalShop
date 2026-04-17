from dataclasses import dataclass
from typing import Final

from domain.common.money import Currency

BASE_CURRENCY: Final[Currency] = Currency.USD
CTX_KEY: Final[str] = "CTX"


@dataclass(slots=True)
class CurrencyRatesCtx:
    related_source_currency: Currency | None = None
    related_target_currency: Currency | None = None
