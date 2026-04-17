from dataclasses import dataclass
from typing import Any

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from domain.common.localized import Language
from presentation.aiogram.setting.category.model import CategorySettings


@dataclass(slots=True, frozen=True)
class LanguageButton:
    lang: Language

    is_current: bool


@inject
async def settings_getter(
    settings: FromDishka[CategorySettings],
    **_: Any,
) -> dict[str, Any]:
    return {"show_with_no_items": settings.show_with_no_items}


@inject
async def default_lang_getter(
    settings: FromDishka[CategorySettings],
    **_: Any,
) -> dict[str, Any]:

    return {
        "buttons": [
            LanguageButton(lang=lang, is_current=settings.default_lang == lang)
            for lang in Language
        ],
    }
