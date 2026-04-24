from decimal import Decimal
from typing import Any

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from app.common.dto.file_key import FileKeyDTO
from app.common.dto.money import MoneyDTO
from app.product.position.cmd import (
    AddPositionMedia,
    AddPositionMediaCmd,
    ChangePositionDescriptionDefaultLang,
    ChangePositionDescriptionDefaultLangCmd,
    ChangePositionNameDefaultLang,
    ChangePositionNameDefaultLangCmd,
    ChangePositionPriceBaseCurrency,
    ChangePositionPriceBaseCurrencyCmd,
    ConvertPositionPriceToOthers,
    ConvertPositionPriceToOthersCmd,
    RemovePositionDescription,
    RemovePositionDescriptionCmd,
    RemovePositionMedia,
    RemovePositionMediaCmd,
    RemovePositionName,
    RemovePositionNameCmd,
    ReplacePositionMedia,
    ReplacePositionMediaCmd,
    SetPositionDescription,
    SetPositionDescriptionCmd,
    SetPositionName,
    SetPositionNameCmd,
    SetPositionPrice,
    SetPositionPriceCmd,
    TranslatePositionDescriptionToOthers,
    TranslatePositionDescriptionToOthersCmd,
    TranslatePositionNameToOthers,
    TranslatePositionNameToOthersCmd,
)
from app.product.position.dto.position import PositionDTO
from app.product.position.query import GetPosition, GetPositionQuery
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.localized import Language
from domain.common.money import Currency
from domain.product.position.exception import PositionDescriptionEmpty
from presentation.aiogram.dialog.admin.position.edit.ctx import (
    CTX_KEY,
    EDIT_POSITION_MEDIA_SCROLL,
    MediaEditingMode,
    PositionEditingCtx,
)
from presentation.aiogram.mapper.file import FileDTOFactory
from presentation.aiogram.port import Text
from presentation.aiogram.setting.position.model import PositionSettings


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    settings: FromDishka[PositionSettings],
) -> None:
    ctx = PositionEditingCtx(
        position_id=data["position_id"],
        current_currency=settings.default_currency,
        current_name_lang=settings.default_lang,
        current_description_lang=settings.default_lang,
        media_mode=MediaEditingMode.ADD,
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_name_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    ctx.current_name_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_edit_name(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    new_name: str,
    retort: FromDishka[Retort],
    handler: FromDishka[SetPositionName],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )

    await handler(
        SetPositionNameCmd(
            id=ctx.position_id,
            lang=ctx.current_name_lang,
            name=new_name,
        ),
    )

    dialog_manager.show_mode = ShowMode.EDIT
    await event.delete()


@inject
async def on_translate_name_to_others(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[TranslatePositionNameToOthers],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )

    await handler(TranslatePositionNameToOthersCmd(id=ctx.position_id))


@inject
async def on_remove_name(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[RemovePositionName],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )

    await handler(
        RemovePositionNameCmd(id=ctx.position_id, lang=ctx.current_name_lang),
    )


@inject
async def on_select_description_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    ctx.current_description_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_edit_description(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    new_description: str,
    retort: FromDishka[Retort],
    handler: FromDishka[SetPositionDescription],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )

    await handler(
        SetPositionDescriptionCmd(
            id=ctx.position_id,
            lang=ctx.current_description_lang,
            description=new_description,
        ),
    )

    dialog_manager.show_mode = ShowMode.EDIT
    await event.delete()


@inject
async def on_translate_description_to_others(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[TranslatePositionDescriptionToOthers],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )

    await handler(TranslatePositionDescriptionToOthersCmd(id=ctx.position_id))


@inject
async def on_remove_description(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[RemovePositionDescription],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )

    await handler(
        RemovePositionDescriptionCmd(
            id=ctx.position_id,
            lang=ctx.current_description_lang,
        ),
    )


@inject
async def on_select_currency(
    event: CallbackQuery,
    widget: Select[Currency],
    dialog_manager: DialogManager,
    currency: Currency,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    ctx.current_currency = currency
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_edit_price(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    new_amount: Decimal,
    retort: FromDishka[Retort],
    handler: FromDishka[SetPositionPrice],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )

    await handler(
        SetPositionPriceCmd(
            id=ctx.position_id,
            money=MoneyDTO(amount=new_amount, currency=ctx.current_currency),
        ),
    )

    dialog_manager.show_mode = ShowMode.EDIT
    await event.delete()


@inject
async def on_change_price_base_currency(
    event: CallbackQuery,
    widget: Select[Currency],
    dialog_manager: DialogManager,
    currency: Currency,
    handler: FromDishka[ChangePositionPriceBaseCurrency],
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )

    await handler(
        ChangePositionPriceBaseCurrencyCmd(
            id=ctx.position_id,
            currency=currency,
        ),
    )


@inject
async def on_convert_price_to_others(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[ConvertPositionPriceToOthers],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )

    await handler(ConvertPositionPriceToOthersCmd(id=ctx.position_id))


@inject
async def on_select_mode(
    event: DialogManager,
    widget: Select[MediaEditingMode],
    dialog_manager: DialogManager,
    mode: MediaEditingMode,
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    ctx.media_mode = mode
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_edit_media(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    add_handler: FromDishka[AddPositionMedia],
    replace_handler: FromDishka[ReplacePositionMedia],
    query_handler: FromDishka[GetPosition],
    factory: FromDishka[FileDTOFactory],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )

    if ctx.media_mode == MediaEditingMode.ADD:
        await add_handler(
            AddPositionMediaCmd(
                id=ctx.position_id,
                media=await factory.from_message(event),
            ),
        )
    else:
        current_page: int = await dialog_manager.find(  # type: ignore[union-attr]
            EDIT_POSITION_MEDIA_SCROLL,
        ).get_page()
        position: PositionDTO = await query_handler(
            GetPositionQuery(id=ctx.position_id),
        )
        if len(position.media) == 0:
            return

        await replace_handler(
            ReplacePositionMediaCmd(
                id=ctx.position_id,
                old_media=position.media[current_page],
                new_media=await factory.from_message(event),
            ),
        )
    await event.delete()
    dialog_manager.show_mode = ShowMode.EDIT


@inject
async def on_change_name_default_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    handler: FromDishka[ChangePositionNameDefaultLang],
    retort: FromDishka[Retort],
) -> None:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    await handler(
        ChangePositionNameDefaultLangCmd(id=ctx.position_id, lang=lang),
    )


@inject
async def on_change_description_default_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    handler: FromDishka[ChangePositionDescriptionDefaultLang],
    text: FromDishka[Text],
    retort: FromDishka[Retort],
) -> None | bool:
    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    try:
        await handler(
            ChangePositionDescriptionDefaultLangCmd(
                id=ctx.position_id,
                lang=lang,
            ),
        )
    except PositionDescriptionEmpty:
        return await event.answer(
            text=text(
                "admin-position-edit-description-default-lang.PositionDescriptionEmpty-call",
            ),
        )

    return None


@inject
async def on_remove_media(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    handler: FromDishka[RemovePositionMedia],
    query_handler: FromDishka[GetPosition],
) -> None:
    scroll: ManagedScroll | None = dialog_manager.find(
        widget_id=EDIT_POSITION_MEDIA_SCROLL,
    )
    if scroll is None:
        return

    ctx: PositionEditingCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        PositionEditingCtx,
    )
    current_page: int = await scroll.get_page()

    position: PositionDTO = await query_handler(
        GetPositionQuery(id=ctx.position_id),
    )
    media_key: FileKeyDTO = position.media[current_page]
    await handler(RemovePositionMediaCmd(id=position.id, media=media_key))

    await scroll.set_page(len(position.media) - 2)
