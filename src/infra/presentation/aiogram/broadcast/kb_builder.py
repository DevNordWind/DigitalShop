from collections.abc import Iterable, Sequence

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from domain.common.localized import Language
from presentation.aiogram.port import Text, TranslatorHub
from presentation.aiogram.port.broadcast.dto import (
    BroadcastButton,
    DataButton,
    I18nText,
    LocalizedText,
    UrlButton,
)


class BroadcastKeyboardBuilder:
    def __init__(self, t_hub: TranslatorHub):
        self._t_hub: TranslatorHub = t_hub
        self._translators: dict[Language, Text] = {}

    def build(
        self,
        lang: Language,
        buttons: Sequence[BroadcastButton],
    ) -> InlineKeyboardMarkup:
        return self.build_many([lang], buttons)[lang]

    def build_many(
        self,
        langs: Iterable[Language],
        buttons: Sequence[BroadcastButton],
    ) -> dict[Language, InlineKeyboardMarkup]:
        generated_kbs: dict[Language, InlineKeyboardMarkup] = {}

        for lang in langs:
            builder = InlineKeyboardBuilder()
            builder.max_width = 1

            if lang not in self._translators:
                self._translators[lang] = self._t_hub(lang)

            if lang not in generated_kbs:
                builder = self._build(
                    lang=lang, builder=builder, buttons=buttons
                )
                markup = builder.as_markup()
                generated_kbs[lang] = markup

        return generated_kbs

    def _build(
        self,
        lang: Language,
        builder: InlineKeyboardBuilder,
        buttons: Sequence[BroadcastButton],
    ) -> InlineKeyboardBuilder:
        for button in buttons:
            if isinstance(button, UrlButton):
                builder.button(text=button.text.texts[lang], url=button.url)
            elif isinstance(button, DataButton):
                text: str
                match button.text:
                    case I18nText():
                        text = self._translators[lang](button.text.key)
                    case LocalizedText():
                        text = button.text.texts[lang]
                builder.button(
                    text=text,
                    callback_data=button.data,
                )
        return builder
