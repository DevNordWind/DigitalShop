from collections.abc import Sequence
from typing import Any

from domain.common.localized import Language
from infra.authentication.telegram.model import TelegramContext
from presentation.aiogram.port import Text, TranslatorHub


class NotificationTextBuilder:
    def __init__(self, t_hub: TranslatorHub):
        self._t_hub: TranslatorHub = t_hub
        self._translators: dict[Language | None, Text] = {}

    async def build(
        self,
        context: TelegramContext,
        key: str,
        **kwargs: Any,
    ) -> dict[Language | None, str]:
        return await self.build_many([context], key, **kwargs)

    async def build_many(
        self,
        contexts: Sequence[TelegramContext],
        key: str,
        **kwargs: Any,
    ) -> dict[Language | None, str]:
        generated_texts: dict[Language | None, str] = {}

        for ctx in contexts:
            if ctx.lang not in self._translators:
                self._translators[ctx.lang] = self._t_hub(ctx.lang)

            if ctx.lang not in generated_texts:
                new_text = self._translators[ctx.lang](key=key, **kwargs)
                generated_texts[ctx.lang] = new_text

        return generated_texts
