import logging
from contextlib import suppress
from typing import Any

from aiogram import Router
from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import (
    CallbackQuery,
    ErrorEvent,
    Message,
    ReplyKeyboardRemove,
    User,
)
from aiogram_dialog import DialogManager, ShowMode
from app.common.exception import ApplicationError
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from domain.common.coefficient import (
    CoefficientTooBig,
    CoefficientTooSmall,
)
from domain.common.exception import DomainError
from presentation.aiogram.port import Text
from presentation.aiogram.state import RootState

logger = logging.getLogger(__name__)


def get_error_router() -> Router:
    error_router = Router()
    error_router.error.register(
        on_domain_application_error,
        ExceptionTypeFilter(DomainError, ApplicationError),
    )
    error_router.error.register(on_unexpected_error)
    return error_router


@inject
async def on_domain_application_error(
    event: ErrorEvent,
    dialog_manager: DialogManager,
    event_context: EventContext,
    text: FromDishka[Text],
    aio_user: FromDishka[User],
) -> Message | bool | None:
    exc: DomainError | ApplicationError = event.exception  # type: ignore[assignment]
    _log_domain_error(event, aio_user, event_context)
    exc_kwargs = _get_exc_kwargs(exc)

    if event.update.message:
        await _reply_to_message(event.update.message, text, exc, exc_kwargs)
        return await dialog_manager.show(show_mode=ShowMode.DELETE_AND_SEND)  # type: ignore[func-returns-value]

    if event.update.callback_query:
        await _answer_callback(
            event.update.callback_query,
            text,
            exc,
            exc_kwargs,
        )
        return None

    logger.warning(
        "Domain/Application error with unhandled update type | update_id=%s | %s",  # noqa: E501
        event.update.update_id,
        exc.__class__.__name__,
    )
    return None


@inject
async def on_unexpected_error(
    event: ErrorEvent,
    dialog_manager: DialogManager,
    event_context: EventContext,
    text: FromDishka[Text],
    aio_user: FromDishka[User],
) -> None:
    logger.error(
        "Unexpected error | %s | user=%s chat=%s | update_id=%s | %s: %s",
        event.update.event_type,
        aio_user.username or aio_user.id,
        event_context.chat_id,
        event.update.update_id,
        event.exception.__class__.__name__,
        event.exception,
        exc_info=(
            type(event.exception),
            event.exception,
            event.exception.__traceback__,
        ),
    )

    if event.update.callback_query:
        await event.update.callback_query.answer(
            text=text("unexpected-error-restart.call"),
            show_alert=True,
        )
        if isinstance(msg := event.update.callback_query.message, Message):
            with suppress(TelegramBadRequest):
                await msg.delete()
            logger.debug(
                "Deleted message after unexpected error | chat=%s",
                event_context.chat_id,
            )

    elif event.update.message:
        await event.update.message.answer(
            text=text("unexpected-error-restart"),
            reply_markup=ReplyKeyboardRemove(),
        )

    logger.info(
        "Restarting dialog to RootState | user=%s chat=%s",
        aio_user.username or aio_user.id,
        event_context.chat_id,
    )
    return await dialog_manager.start(
        state=RootState.root,
    )


async def _reply_to_message(
    message: Message,
    text: Text,
    exc: Exception,
    extra_kwargs: dict[str, Any] | None = None,
) -> None:
    exc_name = exc.__class__.__name__
    kwargs = extra_kwargs or exc.__dict__

    if not text.key_exists(key=exc_name):
        logger.warning(
            "No translation key for %s, falling back to 'unexpected-error'",
            exc_name,
        )
        await message.reply(text=text("unexpected-error"))
    else:
        await message.reply(text=text(key=exc_name, **kwargs))


async def _answer_callback(
    callback: CallbackQuery,
    text: Text,
    exc: Exception,
    extra_kwargs: dict[str, Any] | None = None,
) -> None:
    exc_name = exc.__class__.__name__
    call_key = f"{exc_name}.call"
    kwargs = extra_kwargs or exc.__dict__

    if not text.key_exists(key=call_key):
        logger.warning(
            "No translation key for %s, falling back to 'unexpected-error.call'",  # noqa: E501
            exc_name,
        )
        await callback.answer(
            text=text("unexpected-error.call"),
            show_alert=True,
        )
    else:
        await callback.answer(
            text=text(key=call_key, **kwargs),
            show_alert=True,
        )


def _get_exc_kwargs(exc: Exception) -> dict[str, Any]:
    if isinstance(exc, CoefficientTooSmall):
        return {"min_percent": exc.as_percent}
    if isinstance(exc, CoefficientTooBig):
        return {"max_percent": exc.as_percent}
    return exc.__dict__


def _log_domain_error(
    event: ErrorEvent,
    aio_user: User,
    event_context: EventContext,
) -> None:
    exc = event.exception
    logger.info(
        "Domain/Application error | %s | user=%s chat=%s | update_id=%s | %s",
        event.update.event_type,
        aio_user.username or aio_user.id,
        event_context.chat_id,
        event.update.update_id,
        exc.__class__.__name__,
    )
