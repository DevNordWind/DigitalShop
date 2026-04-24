from dataclasses import dataclass
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from app.product.category.dto.category import CategoryShortDTO
from app.product.category.query import GetCategoryShort, GetCategoryShortQuery
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.localized import Language
from domain.common.money import Currency
from domain.product.position.enums.warehouse import WarehouseType
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.admin.position.create.ctx import (
    CTX_KEY,
    MEDIA_SCROLL,
    PositionCreationCtx,
)
from presentation.aiogram.port import Text
from presentation.aiogram.setting.position.model import PositionSettings


@dataclass(slots=True, frozen=True)
class LanguageButton:
    lang: Language

    is_current: bool


@dataclass(slots=True, frozen=True)
class CurrencyButton:
    currency: Currency

    is_current: bool


@dataclass(slots=True, frozen=True)
class WarehouseButton:
    type: WarehouseType

    is_current: bool


@inject
async def view_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetCategoryShort],
    text: FromDishka[Text],
    settings: FromDishka[PositionSettings],
    tg_ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )

    prices: list[str] = [
        text(
            "position-price-row",
            amount=price.amount,
            currency=price.currency,
            is_last=i == len(ctx.price.prices),
        )
        for i, price in enumerate(ctx.price.prices.values(), start=1)
    ]
    category: CategoryShortDTO = await query_handler(
        GetCategoryShortQuery(ctx.category_id),
    )

    return {
        "name": ctx.name.get(lang=ctx.show_lang),
        "description": ctx.description.get(lang=ctx.show_lang),
        "prices": "\n".join(prices) or None,
        "has_media": bool(ctx.media),
        "has_description": bool(ctx.description.translations),
        "category_name": category.name.get_with_fallback(lang=tg_ctx.lang),
        "buttons": [
            LanguageButton(lang=lang, is_current=lang == ctx.show_lang)
            for lang in Language
        ],
        "can_confirm": settings.is_default_lang_filled(ctx.name)
        and ctx.can_confirm,
    }


@inject
async def input_name_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    settings: FromDishka[PositionSettings],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )
    name = ctx.name.get(lang=ctx.name_current_lang)

    return {
        "name": name,
        "can_translate_to_others": settings.can_translate_to_others(
            localized=ctx.name,
            current_lang=ctx.name_current_lang,
        ),
        "can_clear": ctx.name_current_lang != settings.default_lang
        and name is not None,
        "buttons": [
            LanguageButton(lang=lang, is_current=ctx.name_current_lang == lang)
            for lang in Language
        ],
        "lang": settings.default_lang,
    }


@inject
async def input_description_getter(
    dialog_manager: DialogManager,
    settings: FromDishka[PositionSettings],
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )
    return {
        "description": ctx.description.get(lang=ctx.description_current_lang),
        "can_translate_to_others": settings.can_translate_to_others(
            localized=ctx.description,
            current_lang=ctx.description_current_lang,
        )
        if ctx.description
        else False,
        "buttons": [
            LanguageButton(
                lang=lang,
                is_current=ctx.description_current_lang == lang,
            )
            for lang in Language
        ],
        "lang": settings.default_lang,
    }


@inject
async def input_price_getter(
    dialog_manager: DialogManager,
    settings: FromDishka[PositionSettings],
    retort: FromDishka[Retort],
    text: FromDishka[Text],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )
    prices: list[str] = [
        text(
            "position-price-row",
            amount=price.amount,
            currency=price.currency,
            is_last=i == len(ctx.price.prices),
        )
        for i, price in enumerate(ctx.price.prices.values(), start=1)
    ]

    return {
        "currency": ctx.current_currency,
        "can_convert_to_others": settings.can_convert_to_others(
            price=ctx.price,
            current_currency=ctx.current_currency,
        ),
        "prices": "\n".join(prices) or None,
        "buttons": [
            CurrencyButton(
                currency=currency,
                is_current=currency == ctx.current_currency,
            )
            for currency in Currency
        ],
    }


@inject
async def input_media_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )
    current_page: int = await dialog_manager.find(MEDIA_SCROLL).get_page()  # type: ignore[union-attr]
    media: MediaAttachment | None = None

    if ctx.media:
        media = ctx.media[current_page]

    return {"pages": len(ctx.media), "media": media}


@inject
async def select_warehouse_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )

    return {
        "buttons": [
            WarehouseButton(type=tp, is_current=tp == ctx.warehouse_type)
            for tp in WarehouseType
        ],
    }
