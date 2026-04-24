from dataclasses import dataclass
from typing import Any

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.localized import Language
from domain.common.money import Currency
from presentation.aiogram.setting.position.model import PositionSettings


@dataclass(slots=True, frozen=True)
class LanguageButton:
    lang: Language

    is_current: bool


@dataclass(slots=True, frozen=True)
class CurrencyButton:
    currency: Currency

    is_current: bool


@inject
async def settings_getter(
    settings: FromDishka[PositionSettings],
    **_: Any,
) -> dict[str, bool]:
    return {"show_with_no_items": settings.show_with_no_items}


@inject
async def default_lang_getter(
    settings: FromDishka[PositionSettings],
    **_: Any,
) -> dict[str, Any]:
    return {
        "buttons": [
            LanguageButton(lang=lang, is_current=lang == settings.default_lang)
            for lang in Language
        ],
    }


@inject
async def default_currency_getter(
    settings: FromDishka[PositionSettings],
    **_: Any,
) -> dict[str, Any]:
    return {
        "buttons": [
            CurrencyButton(
                currency=currency,
                is_current=currency == settings.default_currency,
            )
            for currency in Currency
        ],
    }
