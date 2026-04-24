from dataclasses import dataclass
from typing import Any

from dishka.integrations.aiogram_dialog import inject
from domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class CurrencyButton:
    currency: Currency


BUTTONS: tuple[CurrencyButton, ...] = tuple(
    CurrencyButton(currency=currency) for currency in Currency
)


@inject
async def select_currency_getter(
    **_: Any,
) -> dict[str, Any]:
    return {"buttons": BUTTONS}
