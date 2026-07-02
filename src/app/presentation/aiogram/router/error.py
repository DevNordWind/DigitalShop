import logging
from contextlib import suppress
from typing import cast

import structlog
from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import (
    CallbackQuery,
    ErrorEvent,
    Message,
    ReplyKeyboardRemove,
)
from aiogram_dialog import DialogManager, ShowMode
from asgi_correlation_id import correlation_id
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.app.common.exception import (
    AppError,
    AppExternalServiceError,
    AppInfrastructureError,
    BootstrapError,
    DataCorruptionError,
)
from app.domain.common.exception import DomainError
from app.domain.user.enums import UserRole
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.presentation.aiogram.state import RootState
from app.presentation.aiogram.util.error_translator import ErrorTranslator

logger = structlog.get_logger(__name__)


def make_error_router() -> Router:
    error_router = Router()
    error_router.error.register(
        on_app_error,
        ExceptionTypeFilter(AppError),
    )
    error_router.error.register(on_domain_error, ExceptionTypeFilter(DomainError))
    error_router.error.register(on_unexpected_error)
    return error_router


_APP_ERROR_LOG_LEVELS: dict[type[BaseException], int] = {
    DataCorruptionError: logging.CRITICAL,
    BootstrapError: logging.CRITICAL,
    AppInfrastructureError: logging.ERROR,
    AppExternalServiceError: logging.ERROR,
    AppError: logging.WARNING,
}


def _log_app_error(exc: AppError) -> None:
    level = resolve_level_by_hierarchy(
        exc, _APP_ERROR_LOG_LEVELS, default=logging.WARNING
    )
    kwargs: dict[str, object] = {"error_type": exc.__class__.__name__}
    if level >= logging.ERROR:
        kwargs["exc_info"] = exc
    logger.log(level, "app_error", **kwargs)


def _format_admin_notice(exc: AppError) -> str:
    trace_id = correlation_id.get()
    lines = [f"⚠️ {exc.__class__.__name__}"]
    if trace_id:
        lines.append(f"trace_id: {trace_id}")
    return "\n".join(lines)


@inject
async def on_app_error(
    event: ErrorEvent,
    bot: Bot,
    dialog_manager: DialogManager,
    translator: FromDishka[ErrorTranslator],
    ctx: FromDishka[TelegramContextDTO],
) -> Message | bool | None:
    exc: AppError = cast(AppError, event.exception)
    _log_app_error(exc)

    if ctx.user_role >= UserRole.ADMIN:
        await bot.send_message(chat_id=ctx.id, text=_format_admin_notice(exc))

    if event.update.message:
        message: Message = event.update.message
        error_msg: str = translator.translate_error(exc=exc, event=message)
        await message.reply(text=error_msg)
        return await dialog_manager.show(show_mode=ShowMode.DELETE_AND_SEND)

    if event.update.callback_query:
        callback: CallbackQuery = event.update.callback_query
        error_msg = translator.translate_error(exc=exc, event=callback)
        return await callback.answer(error_msg, show_alert=True)

    logger.warning(
        "app_error_unhandled_event_type", update_type=event.update.event_type
    )
    return None


@inject
async def on_domain_error(
    event: ErrorEvent,
    dialog_manager: DialogManager,
    translator: FromDishka[ErrorTranslator],
) -> Message | bool | None:
    exc: DomainError = cast(DomainError, event.exception)

    logger.info("domain_error", error_type=exc.__class__.__name__)

    if event.update.message:
        message: Message = event.update.message
        error_msg: str = translator.translate_error(exc=exc, event=message)
        await message.reply(text=error_msg)
        return await dialog_manager.show(show_mode=ShowMode.DELETE_AND_SEND)

    if event.update.callback_query:
        callback: CallbackQuery = event.update.callback_query
        error_msg = translator.translate_error(exc=exc, event=callback)
        return await callback.answer(error_msg, show_alert=True)

    logger.warning(
        "domain_error_unhandled_event_type", update_type=event.update.event_type
    )
    return None


@inject
async def on_unexpected_error(
    event: ErrorEvent,
    dialog_manager: DialogManager,
    translator: FromDishka[ErrorTranslator],
) -> None:
    logger.error(
        "unexpected_error",
        error_type=event.exception.__class__.__name__,
        exc_info=event.exception,
    )

    if event.update.callback_query:
        error_msg: str = translator.translate_unexpected_error(
            event=event.update.callback_query
        )
        await event.update.callback_query.answer(text=error_msg, show_alert=True)
        if isinstance(msg := event.update.callback_query.message, Message):
            with suppress(TelegramBadRequest):
                await msg.delete()
            logger.debug("message_deleted_after_unexpected_error")

    elif event.update.message:
        error_msg = translator.translate_unexpected_error(event=event.update.message)
        await event.update.message.answer(
            text=error_msg,
            reply_markup=ReplyKeyboardRemove(),
        )

    else:
        logger.warning(
            "unexpected_error_unhandled_event_type",
            update_type=event.update.event_type,
        )

    logger.info("dialog_restarted_to_root")
    return await dialog_manager.start(state=RootState.root)


def resolve_level_by_hierarchy(
    exc: BaseException,
    levels: dict[type[BaseException], int],
    default: int,
) -> int:
    for exc_type in type(exc).__mro__:
        if exc_type in levels:
            return levels[exc_type]
    return default
