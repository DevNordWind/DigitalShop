from dataclasses import dataclass
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.localized import Language

from .ctx import (
    CTX_KEY,
    UrlButtonCtx,
)


@dataclass(slots=True, frozen=True)
class LanguageButton:
    lang: Language

    is_current: bool


@inject
async def url_button_getter(
    dialog_manager: DialogManager, retort: FromDishka[Retort], **_: Any
) -> dict[str, Any]:
    ctx: UrlButtonCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UrlButtonCtx
    )

    return {
        "buttons": [
            LanguageButton(lang=lang, is_current=lang == ctx.show_on)
            for lang in Language
        ],
        "button_url": ctx.url,
        "button_name": ctx.names.get(ctx.show_on),
        "can_create": ctx.can_create,
    }


@inject
async def input_name_getter(
    dialog_manager: DialogManager, retort: FromDishka[Retort], **_: Any
) -> dict[str, Any]:
    ctx: UrlButtonCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UrlButtonCtx
    )

    return {
        "name": ctx.names.get(ctx.current_name_lang),
        "buttons": [
            LanguageButton(lang=lang, is_current=lang == ctx.current_name_lang)
            for lang in Language
        ],
    }


@inject
async def input_url_getter(
    dialog_manager: DialogManager, retort: FromDishka[Retort], **_: Any
) -> dict[str, Any]:
    ctx: UrlButtonCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UrlButtonCtx
    )

    return {"url": ctx.url}
