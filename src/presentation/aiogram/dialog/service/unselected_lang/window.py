from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Select

from domain.common.localized import Language
from presentation.aiogram.state import UnSelectedLangState
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import on_select_lang
from .getter import language_getter

select_lang = Window(
    GetText("unselected-lang"),
    Group(
        Select(
            GetTextSelect("unselected-lang.btn"),
            id="select_lang",
            items="buttons",
            item_id_getter=lambda item: item.lang,
            type_factory=Language,
            on_click=on_select_lang,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    getter=language_getter,
    state=UnSelectedLangState.select_lang,
)
