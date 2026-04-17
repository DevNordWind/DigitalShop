import asyncio
import logging
from contextlib import suppress

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.types import InlineKeyboardMarkup
from dishka import FromDishka
from dishka.integrations.taskiq import inject

from app.common.port.telegram_notification import MessageResult
from app.user.exception import UserAuthenticationError
from infra.authentication.telegram.handler import (
    DeactivateTelegramContext,
    DeactivateTelegramContextCmd,
)
from infra.common.telegram_norification.const import (
    SEND_NOTIFICATION_TASK_NAME,
)
from infra.framework.taskiq.tp import PriorityBroker

logger = logging.getLogger(__name__)


def register_send_notification_task(broker: PriorityBroker) -> None:
    broker.register_task(
        func=send_notification,
        task_name=SEND_NOTIFICATION_TASK_NAME,
        retry_on_error=True,
        max_retries=5,
        delay=0.1,
    )


@inject(patch_module=True)
async def send_notification(
    chat_id: int,
    text: str,
    markup: InlineKeyboardMarkup | None,
    bot: FromDishka[Bot],
    handler: FromDishka[DeactivateTelegramContext],
) -> MessageResult:
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=markup,
        )
        logger.info(f"Sent notification to chat id: {chat_id}")
        return MessageResult.SUCCESS

    except TelegramForbiddenError:
        with suppress(UserAuthenticationError):
            await handler.execute(DeactivateTelegramContextCmd(id=chat_id))
        return MessageResult.NOT_ACTIVE

    except TelegramRetryAfter as e:
        logger.error(e.message)
        await asyncio.sleep(e.retry_after)
        raise

    except Exception as e:
        logger.error(e)
        raise
