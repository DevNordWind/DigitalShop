from typing import Any
from urllib.parse import urlparse

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from domain.common.localized import Language
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.port import Text
from presentation.aiogram.state import CreateUrlButtonState

from .ctx import CTX_KEY, UrlButtonCtx


def validate_url(url: str) -> str:
    parsed = urlparse(url)
    if not bool(parsed.scheme and parsed.netloc):
        raise ValueError("Invalid url")

    return url


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    tg_ctx: FromDishka[TelegramContextDTO],
) -> None:
    if tg_ctx.lang is None:
        return

    ctx = UrlButtonCtx(current_name_lang=tg_ctx.lang, show_on=tg_ctx.lang)
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_name(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    name: str,
    retort: FromDishka[Retort],
) -> None:
    await event.delete()
    dialog_manager.show_mode = ShowMode.EDIT

    ctx: UrlButtonCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UrlButtonCtx
    )
    ctx.names[ctx.current_name_lang] = name
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx: UrlButtonCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UrlButtonCtx
    )
    ctx.show_on = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_name_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    retort: FromDishka[Retort],
) -> None:
    ctx: UrlButtonCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UrlButtonCtx
    )
    ctx.current_name_lang = lang
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_url(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    url: str,
    retort: FromDishka[Retort],
) -> None:
    await event.delete()

    ctx: UrlButtonCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], UrlButtonCtx
    )
    ctx.url = url
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    await dialog_manager.switch_to(
        state=CreateUrlButtonState.url_button, show_mode=ShowMode.EDIT
    )


@inject
async def on_input_url_error(
    event: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    error: ValueError,
    text: FromDishka[Text],
) -> Message:
    return await event.reply(
        text=text("admin-broadcast-buttons-url-url.invalid")
    )


async def on_create(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.done(result=manager.dialog_data[CTX_KEY])
