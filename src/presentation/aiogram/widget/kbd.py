from typing import Any

from aiogram import F
from aiogram.types import InlineKeyboardMarkup
from aiogram_dialog import DialogManager
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import (
    CurrentPage,
    FirstPage,
    Keyboard,
    LastPage,
    NextPage,
    PrevPage,
    Row,
    StubScroll,
)
from aiogram_dialog.widgets.text import Format


class Pagination(Row):
    def __init__(
        self,
        *,
        scroll_id: str,
        prev_text: str = "⬅️",
        next_text: str = "➡️",
        page_format: str = "{current_page1}/{pages}",
    ):
        super().__init__(
            StubScroll(id=scroll_id, pages="pages"),
            PrevPage(
                scroll=scroll_id,
                text=Format(prev_text),
                when=F["current_page"] != 0,
            ),
            FirstPage(
                scroll=scroll_id,
                text=Format(prev_text),
                when=F["current_page"] == 0,
            ),
            CurrentPage(
                scroll=scroll_id,
                text=Format(page_format),
                when=F["pages"] > 1,
            ),
            NextPage(
                scroll=scroll_id,
                text=Format(next_text),
                when=F["current_page1"] != F["pages"],
            ),
            LastPage(
                scroll=scroll_id,
                text=Format(next_text),
                when=F["current_page1"] == F["pages"],
            ),
            when=F["pages"] > 1,
        )


class InlineMarkupWidget(Keyboard):
    def __init__(
        self,
        selector: str,
        id: str | None = None,  # noqa: A002
        when: WhenCondition = None,
    ):
        super().__init__(id, when)
        self.selector: str = selector

    async def _render_keyboard(
        self,
        data: dict[str, Any],
        manager: DialogManager,
    ) -> RawKeyboard:
        """
        Create inline keyboard contents.

        Called if widget is not hidden only (regarding `when`-condition)
        """
        markup = data[self.selector]
        if not isinstance(markup, InlineKeyboardMarkup):
            raise ValueError("Markup must be InlineKeyboardMarkup")

        return markup.inline_keyboard  # type: ignore[return-value]
