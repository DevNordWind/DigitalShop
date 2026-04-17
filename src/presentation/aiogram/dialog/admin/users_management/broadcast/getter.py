from dataclasses import dataclass
from typing import Any

from adaptix import Retort
from aiogram.types import InlineKeyboardMarkup
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from domain.common.localized import Language
from infra.authentication.telegram.dto import TelegramContextDTO
from infra.presentation.aiogram.broadcast.kb_builder import (
    BroadcastKeyboardBuilder,
)
from presentation.aiogram.dialog.admin.users_management.broadcast.ctx import (
    CTX_KEY,
    BroadcastCtx,
)


@dataclass(slots=True, frozen=True)
class LanguageButton:
    lang: Language

    is_current: bool


@dataclass(slots=True, frozen=True)
class UrlButton:
    index: int

    name: str | None
    url: str


PREVIEW_BUTTONS: tuple[LanguageButton, ...] = tuple(
    LanguageButton(lang=lang, is_current=True) for lang in Language
)


@inject
async def broadcast_getter(
    dialog_manager: DialogManager, retort: FromDishka[Retort], **_: Any
) -> dict[str, Any]:
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    return {
        "can_start": ctx.can_start,
    }


async def preview_select_lang_getter(**_: Any) -> dict[str, Any]:
    return {"buttons": PREVIEW_BUTTONS}


@inject
async def preview_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    kb_builder: FromDishka[BroadcastKeyboardBuilder],
    **_: Any,
) -> dict[str, Any]:
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    if ctx.current_preview_lang is None:
        return {}

    markup: InlineKeyboardMarkup = kb_builder.build(
        lang=ctx.current_preview_lang, buttons=ctx.setup.url_buttons
    )
    attachment: MediaAttachment | None = None

    if ctx.setup.media:
        attachment = MediaAttachment(
            type=ctx.setup.media.type,
            file_id=MediaId(
                file_id=ctx.setup.media.file_id,
                file_unique_id=ctx.setup.media.file_unique_id,
            ),
        )

    return {
        "can_start": ctx.can_start,
        "markup": markup,
        "with_close_button": ctx.setup.with_close_button,
        "text": ctx.setup.texts.get(ctx.current_preview_lang),
        "media": attachment,
    }


@inject
async def input_texts_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )

    return {
        "text": ctx.setup.texts.get(ctx.current_texts_lang),
        "buttons": [
            LanguageButton(
                lang=lang, is_current=ctx.current_texts_lang == lang
            )
            for lang in Language
        ],
    }


@inject
async def input_media_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    attachment: MediaAttachment | None = None

    if ctx.setup.media:
        attachment = MediaAttachment(
            type=ctx.setup.media.type,
            file_id=MediaId(
                file_id=ctx.setup.media.file_id,
                file_unique_id=ctx.setup.media.file_unique_id,
            ),
        )

    return {"media": attachment}


@inject
async def buttons_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    tg_ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, Any]:
    ctx: BroadcastCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], BroadcastCtx
    )
    if tg_ctx.lang is None:
        return {}

    return {
        "with_close_button": ctx.setup.with_close_button,
        "buttons": [
            UrlButton(
                index=i, name=url.text.texts.get(tg_ctx.lang), url=url.url
            )
            for i, url in enumerate(ctx.setup.url_buttons)
        ],
    }
