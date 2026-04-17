from typing import Final

from aiogram.types import (
    CopyTextButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from presentation.aiogram.port import Text

COPY_TEXT_LEN: Final[int] = 256


class ServiceKeyboard:
    def __init__(self, text: Text):
        self._text: Text = text

    def get_order_items_markups(
        self,
        items: str,
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        if len(items) <= COPY_TEXT_LEN:
            builder.button(
                text=self._text("inl-ui.copy"),
                copy_text=CopyTextButton(text=items),
            )
        builder.button(
            text=self._text("inl-ui.close"), callback_data="service:close"
        )
        return builder.as_markup()

    def get_tech_work_markup(
        self, support_url: str | None
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        if support_url is not None:
            builder.button(
                text=self._text("tech-work.support-btn"), url=support_url
            )
        builder.button(
            text=self._text("inl-ui.close"), callback_data="service:close"
        )
        return builder.as_markup()

    def get_close_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=self._text("inl-ui.close"),
                        callback_data="service:close",
                    ),
                ],
            ],
        )
