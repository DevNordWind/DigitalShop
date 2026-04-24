from dataclasses import dataclass
from typing import Any

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.localized import Language
from infra.authentication.telegram.dto import TelegramContextDTO


@dataclass(slots=True, frozen=True)
class LanguageButton:
    lang: Language

    is_current: bool


@inject
async def select_lang_getter(
    ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, Any]:
    return {
        "buttons": [
            LanguageButton(lang=lang, is_current=lang == ctx.lang)
            for lang in Language
        ]
    }
