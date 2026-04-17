import asyncio
import logging
from collections.abc import Awaitable
from contextlib import suppress
from typing import Annotated, Any, Final
from uuid import UUID

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramRetryAfter,
)
from aiogram.types import InlineKeyboardMarkup, Message
from dishka import FromDishka
from dishka.integrations.taskiq import inject
from taskiq import AsyncBroker, Context, TaskiqDepends

from app.user.exception import UserAuthenticationError
from infra.authentication.telegram.handler import (
    DeactivateTelegramContext,
    DeactivateTelegramContextCmd,
)
from infra.framework.taskiq.tp import PriorityBroker
from infra.presentation.aiogram.broadcast.const import (
    SEND_MSG_TASK_NAME,
    UPDATE_PROGRESS_TASK_NAME,
)
from infra.presentation.aiogram.broadcast.dto import (
    BroadcastProgress,
    MessageResult,
)
from infra.presentation.aiogram.broadcast.limiter import BroadcastRateLimiter
from infra.presentation.aiogram.broadcast.progress import (
    BroadcastProgressGateway,
    BroadcastProgressMessage,
)
from presentation.aiogram.port.broadcast.dto import (
    BroadcastMedia,
    BroadcastReporting,
)

logger = logging.getLogger(__name__)

SEND_MSG_MAX_RETRIES: Final[int] = 3


def register_send_msg_task(broker: AsyncBroker) -> None:
    broker.register_task(
        func=send_message,
        task_name=SEND_MSG_TASK_NAME,
        retry_on_error=True,
        max_retries=SEND_MSG_MAX_RETRIES,
        delay=0.1,
    )


def register_update_progress_task(broker: PriorityBroker) -> None:
    broker.register_task(
        func=update_progress,
        task_name=UPDATE_PROGRESS_TASK_NAME,
        delay=0.1,
        retry_on_error=True,
        max_retries=10,
    )


@inject(patch_module=True)
async def update_progress(
    broadcast_id: UUID,
    reporting: BroadcastReporting,
    message: FromDishka[BroadcastProgressMessage],
    gateway: FromDishka[BroadcastProgressGateway],
    broker: FromDishka[PriorityBroker],
) -> None:
    current_progress: BroadcastProgress | None = await gateway.get(
        broadcast_id=broadcast_id
    )
    if not current_progress:
        return

    msg: Message | None = None
    try:
        msg = await message.update(
            reporting=reporting, progress=current_progress
        )
    except TelegramBadRequest as e:
        if "message is not modified" in e.message:
            pass
    if current_progress.current >= current_progress.total:
        await gateway.delete(broadcast_id=broadcast_id)
        return

    if msg and msg.message_id != current_progress.current_message_id:
        await gateway.set_current_message_id(
            broadcast_id=broadcast_id, message_id=msg.message_id
        )

    task = broker.find_task(UPDATE_PROGRESS_TASK_NAME)
    if not task:
        raise RuntimeError(f"Task {UPDATE_PROGRESS_TASK_NAME} not found")

    await asyncio.sleep(5)
    await task.kicker().with_labels(delay=3).kiq(broadcast_id, reporting)


@inject(patch_module=True)
async def send_message(
    broadcast_id: UUID,
    chat_id: int,
    text: str,
    markup: InlineKeyboardMarkup | None,
    media: BroadcastMedia | None,
    bot: FromDishka[Bot],
    handler: FromDishka[DeactivateTelegramContext],
    limiter: FromDishka[BroadcastRateLimiter],
    progress_gw: FromDishka[BroadcastProgressGateway],
    context: Annotated[Context, TaskiqDepends()],
) -> MessageResult:
    await limiter.acquire()
    result: MessageResult

    try:
        await _resolve_send_method(
            chat_id=chat_id, text=text, markup=markup, media=media, bot=bot
        )
        logger.info(f"Sent message to chat id: {chat_id}")
        result = MessageResult.SUCCESS

    except TelegramBadRequest as e:
        result = MessageResult.ERROR
        logger.error(e)

    except TelegramForbiddenError:
        with suppress(UserAuthenticationError):
            await handler.execute(DeactivateTelegramContextCmd(id=chat_id))
        result = MessageResult.NOT_ACTIVE

    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        raise

    except Exception as e:
        result = MessageResult.ERROR
        retries: int = context.message.labels.get("_retries", 0)

        if retries >= SEND_MSG_MAX_RETRIES:
            await progress_gw.incr(broadcast_id, result)
            return result
        logger.error(
            f"Exception: {e}, retries: {retries}, max: {SEND_MSG_MAX_RETRIES}"
        )
        raise

    await progress_gw.incr(broadcast_id, result)
    return result


def _resolve_send_method(
    bot: Bot,
    chat_id: int,
    text: str,
    markup: InlineKeyboardMarkup | None,
    media: BroadcastMedia | None,
) -> Awaitable[Any]:
    if media is None:
        return bot.send_message(
            chat_id=chat_id, text=text, reply_markup=markup
        )

    match media.type:
        case ContentType.PHOTO:
            return bot.send_photo(
                chat_id=chat_id,
                caption=text,
                photo=media.file_id,
                reply_markup=markup,
            )
        case ContentType.VIDEO:
            return bot.send_video(
                chat_id=chat_id,
                caption=text,
                video=media.file_id,
                reply_markup=markup,
            )
        case ContentType.ANIMATION:
            return bot.send_animation(
                chat_id=chat_id,
                caption=text,
                animation=media.file_id,
                reply_markup=markup,
            )
        case _:
            raise ValueError(f"Unsupported ContentType: {media.type}")
