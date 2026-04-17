from dataclasses import dataclass
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from domain.common.localized import Language
from presentation.aiogram.dialog.admin.category.create.ctx import (
    CTX_KEY,
    CategoryCreationContext,
)
from presentation.aiogram.setting.category.model import CategorySettings


@dataclass(slots=True, frozen=True)
class LanguageButton:
    lang: Language
    is_current: bool


@inject
async def view_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    settings: FromDishka[CategorySettings],
    **_: Any,
) -> dict[str, Any]:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )

    return {
        "name": ctx.name.get(ctx.show_lang),
        "description": ctx.description.get(ctx.show_lang),
        "has_media": bool(ctx.media),
        "buttons": [
            LanguageButton(lang=lang, is_current=ctx.show_lang == lang)
            for lang in Language
        ],
        "has_description": bool(ctx.description.translations),
        "media": ctx.media,
        "can_create": settings.is_default_lang_filled(localized=ctx.name),
    }


@inject
async def input_name_getter(
    dialog_manager: DialogManager,
    settings: FromDishka[CategorySettings],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )

    return {
        "buttons": [
            LanguageButton(lang=lang, is_current=ctx.name_current_lang == lang)
            for lang in Language
        ],
        "name": ctx.name.get(lang=ctx.name_current_lang),
        "lang": settings.default_lang,
        "can_translate_to_others": settings.can_translate_to_others(
            localized=ctx.name,
            current_lang=ctx.name_current_lang,
        ),
    }


@inject
async def input_description_getter(
    dialog_manager: DialogManager,
    settings: FromDishka[CategorySettings],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )

    return {
        "buttons": [
            LanguageButton(
                lang=lang,
                is_current=ctx.description_current_lang == lang,
            )
            for lang in Language
        ],
        "has_description": bool(ctx.description.translations),
        "description": ctx.description.get(lang=ctx.description_current_lang),
        "can_translate_to_others": settings.can_translate_to_others(
            localized=ctx.description,
            current_lang=ctx.name_current_lang,
        ),
        "lang": settings.default_lang,
    }


@inject
async def input_media_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryCreationContext,
    )

    return {"media": ctx.media}
