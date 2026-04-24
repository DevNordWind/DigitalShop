from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Group, Select
from domain.common.localized import Language
from presentation.aiogram.state import LanguageState
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import on_select_lang
from .getter import select_lang_getter

select_lang = Window(
    GetText("user-select-lang"),
    Group(
        Select(
            GetTextSelect("user-select-lang.btn"),
            id="select_lang",
            type_factory=Language,
            items="buttons",
            on_click=on_select_lang,  # type: ignore[arg-type]
            item_id_getter=lambda item: item.lang,
        ),
        width=2,
    ),
    Cancel(
        GetText("inl-ui.back"),
    ),
    state=LanguageState.select_lang,
    getter=select_lang_getter,
)
