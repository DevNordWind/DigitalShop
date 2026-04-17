import asyncio
from collections.abc import Awaitable
from decimal import Decimal
from typing import Any

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import (
    ManagedTextInput,
    MessageInput,
    TextInput,
)
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.file_key import FileKeyRawDTO
from app.common.dto.localized import LocalizedTextDTO
from app.common.dto.money import MoneyDTO, MoneyMapper
from app.common.port import Translator
from app.product.position.cmd import CreatePosition, CreatePositionCmd
from app.product.position.dto.description.mapper import (
    PositionDescriptionMapper,
)
from app.product.position.dto.name import PositionNameMapper
from app.product.position.dto.price import PositionPriceDTO
from domain.common.exchange_rate import CurrencyPair, ExchangeRateGateway
from domain.common.localized import Language
from domain.common.money import Currency, Money
from domain.product.position.enums.warehouse import WarehouseType
from presentation.aiogram.dialog.admin.position.create.ctx import (
    CTX_KEY,
    MEDIA_SCROLL,
    PositionCreationCtx,
)
from presentation.aiogram.mapper.file import FileDTOFactory
from presentation.aiogram.mapper.media_attachment import (
    MediaAttachmentFactory,
)
from presentation.aiogram.setting.position.model import PositionSettings


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    settings: FromDishka[PositionSettings],
) -> None:
    localized_text = LocalizedTextDTO(
        default_lang=settings.default_lang,
        translations={},
    )
    ctx = PositionCreationCtx(
        category_id=dialog_manager.start_data["category_id"],  # type: ignore[index, call-overload,arg-type]
        name=localized_text,
        description=localized_text,
        media=[],
        price=PositionPriceDTO(
            base_currency=settings.default_currency,
            prices={},
        ),
        show_lang=settings.default_lang,
        name_current_lang=settings.default_lang,
        warehouse_type=None,
        description_current_lang=settings.default_lang,
        current_currency=settings.default_currency,
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_language(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(dialog_manager.dialog_data[CTX_KEY], PositionCreationCtx)
    ctx.show_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_name(
    event: Message,
    widget: TextInput[str],
    dialog_manager: DialogManager,
    name: str,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )
    ctx.name.translations[ctx.name_current_lang] = name

    PositionNameMapper.to_value_object(src=ctx.name)

    await event.delete()
    dialog_manager.show_mode = ShowMode.EDIT

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_clear_name(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(dialog_manager.dialog_data[CTX_KEY], PositionCreationCtx)
    ctx.name.translations.pop(ctx.name_current_lang)

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_name_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(dialog_manager.dialog_data[CTX_KEY], PositionCreationCtx)
    ctx.name_current_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_description(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    description: str,
    retort: FromDishka[Retort],
) -> None | Message:
    ctx = retort.load(dialog_manager.dialog_data[CTX_KEY], PositionCreationCtx)
    ctx.description.translations[ctx.description_current_lang] = description

    PositionDescriptionMapper.to_value_object(src=ctx.description)

    await event.delete()
    dialog_manager.show_mode = ShowMode.EDIT
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    return None


@inject
async def on_clear_description(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(dialog_manager.dialog_data[CTX_KEY], PositionCreationCtx)
    ctx.description.translations.pop(ctx.description_current_lang)

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_description_lang(
    event: CallbackQuery,
    select: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(dialog_manager.dialog_data[CTX_KEY], PositionCreationCtx)
    ctx.description_current_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_media(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )
    ctx.media.append(MediaAttachmentFactory.from_message(msg=event))
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    await event.delete()
    dialog_manager.show_mode = ShowMode.EDIT


@inject
async def on_remove_media(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )
    current_page: int = await dialog_manager.find(MEDIA_SCROLL).get_page()  # type: ignore[union-attr]
    ctx.media.pop(current_page)

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_confirm(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[CreatePosition],
    file_factory: FromDishka[FileDTOFactory],
) -> None | bool:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )
    if ctx.warehouse_type is None:
        return None

    position_media: list[FileKeyRawDTO] = [
        await file_factory.from_media_attachment(attachment)
        for attachment in ctx.media
    ]

    await handler(
        CreatePositionCmd(
            category_id=ctx.category_id,
            name=ctx.name,
            description=ctx.description
            if ctx.description.translations
            else None,
            media=position_media,
            price=ctx.price,
            warehouse_type=ctx.warehouse_type,
        ),
    )

    await dialog_manager.done()

    return None


@inject
async def on_translate_name_to_others(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    translator: FromDishka[Translator],
    retort: FromDishka[Retort],
    settings: FromDishka[PositionSettings],
) -> None:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )
    source_text: str = ctx.name.translations[settings.default_lang]

    coroutines: dict[Language, Awaitable[str]] = {}
    for lang in Language:
        if lang != settings.default_lang:
            coroutines[lang] = translator.translate(
                source=settings.default_lang,
                target=lang,
                text=source_text,
            )

    results: list[str] = await asyncio.gather(*(tuple(coroutines.values())))

    translations: dict[Language, str] = dict(
        zip(coroutines.keys(), results, strict=True),
    )

    ctx.name = LocalizedTextDTO(
        default_lang=settings.default_lang,
        translations=dict(translations.items())
        | {settings.default_lang: source_text},
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_translate_description_to_others(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    translator: FromDishka[Translator],
    retort: FromDishka[Retort],
    settings: FromDishka[PositionSettings],
) -> None:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )
    source_text: str = ctx.description.translations[settings.default_lang]

    coroutines: dict[Language, Awaitable[str]] = {}
    for lang in Language:
        if lang != settings.default_lang:
            coroutines[lang] = translator.translate(
                source=settings.default_lang,
                target=lang,
                text=source_text,
            )

    results: list[str] = await asyncio.gather(*(tuple(coroutines.values())))

    translations: dict[Language, str] = dict(
        zip(coroutines.keys(), results, strict=True),
    )

    ctx.description = LocalizedTextDTO(
        default_lang=settings.default_lang,
        translations=dict(translations.items())
        | {settings.default_lang: source_text},
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_price(
    event: Message,
    widget: ManagedTextInput[Decimal],
    dialog_manager: DialogManager,
    amount: Decimal,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )

    money = Money(amount=amount, currency=ctx.current_currency)

    ctx.price.prices[ctx.current_currency] = MoneyMapper.to_dto(money)

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    await event.delete()
    dialog_manager.show_mode = ShowMode.EDIT


@inject
async def on_select_currency(
    event: CallbackQuery,
    select: Select[Currency],
    dialog_manager: DialogManager,
    currency: Currency,
    retort: FromDishka[Retort],
) -> None:
    ctx = retort.load(dialog_manager.dialog_data[CTX_KEY], PositionCreationCtx)
    ctx.current_currency = currency
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_convert_price_to_others(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    rate_gateway: FromDishka[ExchangeRateGateway],
    settings: FromDishka[PositionSettings],
) -> None:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )
    source: MoneyDTO = ctx.price.prices[settings.default_currency]

    source_v_o = MoneyMapper.to_value_object(source)

    pairs = [
        CurrencyPair(source=source.currency, target=currency)
        for currency in Currency
        if currency != source.currency
    ]

    rates = await rate_gateway.get_many(pairs)

    ctx.price = PositionPriceDTO(
        base_currency=settings.default_currency,
        prices={
            rate.pair.target: MoneyMapper.to_dto(src=rate.convert(source_v_o))
            for rate in rates
        }
        | {source.currency: source},
    )

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_warehouse(
    event: CallbackQuery,
    widget: Select[WarehouseType],
    dialog_manager: DialogManager,
    tp: WarehouseType,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionCreationCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionCreationCtx,
    )
    ctx.warehouse_type = tp

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
