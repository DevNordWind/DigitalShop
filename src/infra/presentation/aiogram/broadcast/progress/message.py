from contextlib import suppress
from dataclasses import dataclass

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from infra.presentation.aiogram.broadcast.dto import (
    BroadcastProgress,
)
from infra.presentation.aiogram.broadcast.kb_builder import (
    BroadcastKeyboardBuilder,
)
from presentation.aiogram.port import Text, TranslatorHub
from presentation.aiogram.port.broadcast.dto import (
    DEFAULT_CLOSE_BUTTON,
    BroadcastReporting,
)


@dataclass(slots=True, frozen=True)
class BroadcastProgressConfig:
    start_msg_key: str = "broadcast-started"
    progress_msg_key: str = "broadcast-in-progress"
    ended_msg_key: str = "broadcast-ended"


class BroadcastProgressMessage:
    def __init__(
        self,
        bot: Bot,
        t_hub: TranslatorHub,
        config: BroadcastProgressConfig,
        kb_builder: BroadcastKeyboardBuilder,
    ):
        self.config: BroadcastProgressConfig = config
        self._bot: Bot = bot
        self._t_hub: TranslatorHub = t_hub
        self._kb_builder: BroadcastKeyboardBuilder = kb_builder

    async def start(
        self, reporting: BroadcastReporting, total: int
    ) -> Message:
        text: Text = self._t_hub(reporting.report_lang)

        return await self._bot.send_message(
            chat_id=reporting.report_to,
            text=text(self.config.start_msg_key, total=total),
        )

    async def update(
        self, reporting: BroadcastReporting, progress: BroadcastProgress
    ) -> Message | None:
        text: Text = self._t_hub(reporting.report_lang)

        built_text: str = text(
            self.config.progress_msg_key,
            total=progress.total,
            success=progress.success,
            error=progress.error,
            not_active=progress.not_active,
            current=progress.current,
        )
        if progress.current >= progress.total:
            await self.end(reporting, progress)
            return None

        try:
            msg = await self._bot.edit_message_text(
                text=built_text,
                message_id=progress.current_message_id,
                chat_id=reporting.report_to,
            )
            if isinstance(msg, Message):
                return msg
        except TelegramBadRequest as e:
            if "message to edit not found" in e.message:
                return await self._bot.send_message(
                    chat_id=reporting.report_to,
                    text=built_text,
                )
            raise

        return None

    async def end(
        self,
        reporting: BroadcastReporting,
        current_progress: BroadcastProgress,
    ) -> None:
        if current_progress.current_message_id is None:
            raise ValueError("Message not found")

        with suppress(TelegramBadRequest):
            await self._bot.delete_message(
                chat_id=reporting.report_to,
                message_id=current_progress.current_message_id,
            )
        text = self._t_hub(reporting.report_lang)

        await self._bot.send_message(
            chat_id=reporting.report_to,
            text=text(
                self.config.ended_msg_key,
                total=current_progress.total,
                success=current_progress.success,
                error=current_progress.error,
                not_active=current_progress.not_active,
            ),
            reply_markup=(
                self._kb_builder.build(
                    lang=reporting.report_lang, buttons=[DEFAULT_CLOSE_BUTTON]
                )
            ),
        )
