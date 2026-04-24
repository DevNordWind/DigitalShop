from dataclasses import dataclass
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from app.common.dto.file_key import FileKeyMapper as AppFileKeyMapper
from app.common.dto.localized import LocalizedTextDTO
from app.product.position.dto.position import PositionDTO
from app.product.position.query import GetPosition, GetPositionQuery
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.localized import Language
from domain.common.money import Currency
from presentation.aiogram.dialog.admin.position.edit.ctx import (
    CTX_KEY,
    EDIT_POSITION_MEDIA_SCROLL,
    MediaEditingMode,
    PositionEditingCtx,
)
from presentation.aiogram.mapper import FileKeyMapper
from presentation.aiogram.port import Text


@dataclass(slots=True, frozen=True)
class LanguageButton:
    lang: Language

    is_current: bool


@dataclass(slots=True, frozen=True)
class CurrencyButton:
    currency: Currency

    is_current: bool


@dataclass(slots=True, frozen=True)
class MediaModeButton:
    mode: MediaEditingMode

    is_current: bool


@inject
async def edit_name_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetPosition],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    position: PositionDTO = await query_handler(
        GetPositionQuery(id=ctx.position_id),
    )

    return {
        "buttons": [
            LanguageButton(lang=lang, is_current=lang == ctx.current_name_lang)
            for lang in Language
        ],
        "name": position.name.get(lang=ctx.current_name_lang),
        "can_translate_to_others": ctx.current_name_lang
        == position.name.default_lang
        and len(position.name.translations) != len(Language),
        "can_remove": ctx.current_name_lang != position.name.default_lang
        and position.name.get(ctx.current_name_lang) is not None,
        "lang": position.name.default_lang,
    }


@inject
async def edit_name_default_lang(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetPosition],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    position: PositionDTO = await query_handler(
        GetPositionQuery(id=ctx.position_id),
    )
    return {
        "buttons": [
            LanguageButton(
                lang=lang,
                is_current=position.name.default_lang == lang,
            )
            for lang in Language
        ],
        "lang": position.name.default_lang,
    }


@inject
async def edit_description_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetPosition],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    position: PositionDTO = await query_handler(
        GetPositionQuery(id=ctx.position_id),
    )

    description: str | None = None
    can_translate_to_others: bool = False
    default_lang: Language | None = None
    if isinstance(position.description, LocalizedTextDTO):
        description = position.description.get(
            lang=ctx.current_description_lang,
        )
        can_translate_to_others = (
            ctx.current_description_lang == position.description.default_lang
            and len(position.description.translations) != len(Language)
        )
        default_lang = position.description.default_lang

    return {
        "buttons": [
            LanguageButton(
                lang=lang,
                is_current=lang == ctx.current_description_lang,
            )
            for lang in Language
        ],
        "description": description,
        "can_translate_to_others": can_translate_to_others,
        "can_change_default_lang": position.description is not None,
        "has_description": position.description is not None,
        "lang": default_lang,
    }


@inject
async def edit_description_default_lang(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetPosition],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    position: PositionDTO = await query_handler(
        GetPositionQuery(id=ctx.position_id),
    )
    return {
        "buttons": [
            LanguageButton(
                lang=lang,
                is_current=position.description.default_lang == lang
                if position.description
                else False,
            )
            for lang in Language
        ],
    }


@inject
async def edit_price_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetPosition],
    retort: FromDishka[Retort],
    text: FromDishka[Text],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    position: PositionDTO = await query_handler(
        GetPositionQuery(id=ctx.position_id),
    )
    prices: list[str] = [
        text(
            "position-price-row",
            amount=price.amount,
            currency=price.currency,
            is_last=i == len(position.price.prices),
        )
        for i, price in enumerate(position.price.prices.values(), start=1)
    ]

    return {
        "buttons": [
            CurrencyButton(
                currency=currency,
                is_current=currency == ctx.current_currency,
            )
            for currency in Currency
        ],
        "can_convert_to_others": position.price.base_currency
        == ctx.current_currency,
        "can_remove": position.price.base_currency != ctx.current_currency,
        "prices": "\n".join(prices),
    }


@inject
async def edit_price_base_currency_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetPosition],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    position: PositionDTO = await query_handler(
        GetPositionQuery(id=ctx.position_id),
    )

    return {
        "buttons": [
            CurrencyButton(
                currency=currency,
                is_current=position.price.base_currency == currency,
            )
            for currency in Currency
        ],
    }


@inject
async def edit_media_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetPosition],
    mapper: FromDishka[FileKeyMapper],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    position: PositionDTO = await query_handler(
        GetPositionQuery(id=ctx.position_id),
    )
    current_page: int = await dialog_manager.find(  # type: ignore[union-attr]
        EDIT_POSITION_MEDIA_SCROLL,
    ).get_page()

    media: MediaAttachment | None = None
    if position.media:
        media = await mapper.to_media_attachment(
            key=AppFileKeyMapper.to_value_object(
                src=position.media[current_page],
            ),
        )

    return {
        "media": media,
        "pages": len(position.media),
        "buttons": [
            MediaModeButton(mode=mode, is_current=mode == ctx.media_mode)
            for mode in MediaEditingMode
        ],
    }
