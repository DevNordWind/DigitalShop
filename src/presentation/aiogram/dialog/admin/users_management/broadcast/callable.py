import asyncio
from typing import Any

from adaptix import Retort
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Data, DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from domain.common.localized import Language
from infra.authentication.telegram.dto import TelegramContextDTO
from infra.authentication.telegram.model import TelegramId
from presentation.aiogram.dialog.admin.users_management.broadcast.ctx import (
    CTX_KEY,
    BroadcastCtx,
    BroadcastSetup,
)
from presentation.aiogram.port import Text
from presentation.aiogram.port.broadcast import (
    BroadcastMedia,
    BroadcastRequest,
    TelegramBroadcaster,
)
from presentation.aiogram.port.broadcast.dto import (
    DEFAULT_CLOSE_BUTTON,
    BroadcastButton,
    BroadcastReporting,
    LocalizedText,
    UrlButton,
)
from presentation.aiogram.port.broadcast.exception import BroadcastTextsAsymmetrically
from presentation.aiogram.state import BroadcastState

from .url_button.ctx import UrlButtonCtx


@inject
async def on_start(
    data: Data,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    tg_ctx: FromDishka[TelegramContextDTO],
) -> None:
    if tg_ctx.lang is None:
        return

    ctx = BroadcastCtx(
        current_preview_lang=None,
        current_texts_lang=tg_ctx.lang,
        setup=BroadcastSetup(
            media=None,
            texts={},
            url_buttons=[],
        ),
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_preview_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    ctx.current_preview_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    await dialog_manager.switch_to(state=BroadcastState.preview)


@inject
async def on_select_texts_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    ctx.current_texts_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_text(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    text: str,
    retort: FromDishka[Retort],
) -> None:
    await event.delete()
    dialog_manager.show_mode = ShowMode.EDIT

    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    ctx.setup.texts[ctx.current_texts_lang] = text
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_remove_text(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    ctx.setup.texts.pop(ctx.current_texts_lang)
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_switch_close_button(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    ctx.setup.with_close_button = not ctx.setup.with_close_button
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_media(
    event: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    await event.delete()
    dialog_manager.show_mode = ShowMode.EDIT
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    media: BroadcastMedia

    if event.photo:
        media = BroadcastMedia(
            type=ContentType.PHOTO,
            file_id=event.photo[-1].file_id,
            file_unique_id=event.photo[-1].file_unique_id,
        )
    elif event.video:
        media = BroadcastMedia(
            type=ContentType.VIDEO,
            file_id=event.video.file_id,
            file_unique_id=event.video.file_unique_id,
        )
    elif event.animation:
        media = BroadcastMedia(
            type=ContentType.VIDEO,
            file_id=event.animation.file_id,
            file_unique_id=event.animation.file_unique_id,
        )
    else:
        return
    ctx.setup.media = media
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_clear_media(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    ctx.setup.media = None
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def url_process_result(
    start_data: Data,
    result: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    if not isinstance(result, dict):
        return

    url_ctx: UrlButtonCtx = retort.load(result, UrlButtonCtx)
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    if url_ctx.url is None:
        raise ValueError
    ctx.setup.url_buttons.append(
        UrlButton(
            text=LocalizedText(
                texts=url_ctx.names,
            ),
            url=url_ctx.url,
        )
    )
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_start_broadcast(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    broadcaster: FromDishka[TelegramBroadcaster],
    retort: FromDishka[Retort],
    tg_ctx: FromDishka[TelegramContextDTO],
    t: FromDishka[Text]
) -> bool | None:
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    if tg_ctx.lang is None:
        return

    buttons: list[BroadcastButton] = []
    buttons.extend(ctx.setup.url_buttons)
    if ctx.setup.with_close_button:
        buttons.append(DEFAULT_CLOSE_BUTTON)
    try:
        await broadcaster.broadcast(
            request=BroadcastRequest(
                texts=LocalizedText(
                    texts=ctx.setup.texts,
                ),
                reporting=BroadcastReporting(
                    report_to=TelegramId(tg_ctx.id), report_lang=tg_ctx.lang
                ),
                media=ctx.setup.media,
                buttons=tuple(buttons),
            )
        )
    except BroadcastTextsAsymmetrically as e:
        return await event.answer(
            text=t(e.__class__.__name__)
        )

    await dialog_manager.done()


@inject
async def on_delete_url_button(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    ctx.setup.url_buttons.pop(int(dialog_manager.item_id))  # type: ignore[attr-defined]
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
