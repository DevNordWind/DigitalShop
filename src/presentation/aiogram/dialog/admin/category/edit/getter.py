from dataclasses import dataclass
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.file_key import FileKeyMapper as AppFileKeyMapper
from app.common.dto.localized import LocalizedTextDTO
from app.product.category.dto.category import CategoryDTO
from app.product.category.query import GetCategory, GetCategoryQuery
from domain.common.file import FileKey
from domain.common.localized import Language
from presentation.aiogram.dialog.admin.category.edit.ctx import (
    CTX_KEY,
    CategoryEditingCtx,
)
from presentation.aiogram.mapper import FileKeyMapper


@dataclass(slots=True, frozen=True)
class LanguageButton:
    lang: Language
    is_current: bool


@inject
async def edit_name_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetCategory],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    dto: CategoryDTO = await query_handler(
        GetCategoryQuery(id=ctx.category_id),
    )

    return {
        "name": dto.name.get(lang=ctx.current_name_lang),
        "buttons": [
            LanguageButton(lang=lang, is_current=lang == ctx.current_name_lang)
            for lang in Language
        ],
        "can_translate_to_others": dto.name.default_lang
        == ctx.current_name_lang
        and len(dto.name.translations) != len(Language),
        "can_remove": dto.name.default_lang != ctx.current_name_lang,
        "lang": dto.name.default_lang,
    }


@inject
async def edit_name_default_lang_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetCategory],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )
    dto: CategoryDTO = await query_handler(
        GetCategoryQuery(id=ctx.category_id),
    )

    return {
        "buttons": [
            LanguageButton(lang=lang, is_current=lang == dto.name.default_lang)
            for lang in Language
        ],
    }


@inject
async def edit_description_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetCategory],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )
    dto: CategoryDTO = await query_handler(
        GetCategoryQuery(id=ctx.category_id),
    )

    description: str | None = None
    can_translate_to_others: bool = False
    default_lang: Language | None = None

    if isinstance(dto.description, LocalizedTextDTO):
        description = dto.description.get(lang=ctx.current_description_lang)
        can_translate_to_others = (
            dto.description.default_lang == ctx.current_description_lang
            and len(dto.description.translations) != len(Language)
        )
        default_lang = dto.description.default_lang

    return {
        "buttons": [
            LanguageButton(
                lang=lang,
                is_current=lang == ctx.current_description_lang,
            )
            for lang in Language
        ],
        "lang": default_lang,
        "has_description": description is not None,
        "can_translate_to_others": can_translate_to_others,
        "description": description,
    }


@inject
async def edit_description_default_lang_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetCategory],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )
    dto: CategoryDTO = await query_handler(
        GetCategoryQuery(id=ctx.category_id),
    )

    return {
        "buttons": [
            LanguageButton(
                lang=lang,
                is_current=lang == dto.description.default_lang
                if dto.description
                else False,
            )
            for lang in Language
        ],
    }


@inject
async def edit_media_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetCategory],
    mapper: FromDishka[FileKeyMapper],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: CategoryEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        CategoryEditingCtx,
    )

    category: CategoryDTO = await query_handler(
        GetCategoryQuery(id=ctx.category_id),
    )
    attachment: MediaAttachment | None = None
    if category.media is not None:
        key: FileKey = AppFileKeyMapper.to_value_object(src=category.media)
        attachment = await mapper.to_media_attachment(key=key)

    return {"media": attachment}
