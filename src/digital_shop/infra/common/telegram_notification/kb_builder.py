from collections.abc import Sequence

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.common.port.telegram_notification import Button
from domain.common.localized import Language
from infra.authentication.telegram.model import TelegramContext
from presentation.aiogram.port import Text, TranslatorHub


class NotificationKeyboardBuilder:
    def __init__(self, t_hub: TranslatorHub):
        self._t_hub: TranslatorHub = t_hub
        self._translators: dict[Language | None, Text] = {}

    async def build(
        self,
        context: TelegramContext,
        buttons: list[Button],
    ) -> dict[Language | None, InlineKeyboardMarkup]:
        return await self.build_many([context], buttons)

    async def build_many(
        self,
        contexts: Sequence[TelegramContext],
        buttons: list[Button],
    ) -> dict[Language | None, InlineKeyboardMarkup]:
        generated_kbs: dict[Language | None, InlineKeyboardMarkup] = {}

        for ctx in contexts:
            builder = InlineKeyboardBuilder()

            if ctx.lang not in self._translators:
                self._translators[ctx.lang] = self._t_hub(ctx.lang)

            if ctx.lang not in generated_kbs:
                for button in buttons:
                    builder.button(
                        text=self._translators[ctx.lang](button.key),
                        callback_data=button.data,
                    )
                markup = builder.as_markup()
                generated_kbs[ctx.lang] = markup

        return generated_kbs
