from aiogram.enums import ButtonStyle
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Group, Select, SwitchTo
from aiogram_dialog.widgets.style import Style
from domain.common.localized import Language
from presentation.aiogram.dialog.admin.category.settings.callable import (
    on_change_default_lang,
    on_switch_with_no_items,
)
from presentation.aiogram.dialog.admin.category.settings.getter import (
    default_lang_getter,
    settings_getter,
)
from presentation.aiogram.state import CategorySettingsState
from presentation.aiogram.widget import GetText, GetTextSelect

settings = Window(
    GetText("admin-category-settings"),
    SwitchTo(
        GetText("admin-category-settings.default-lang-btn"),
        id="to_default_lang",
        state=CategorySettingsState.default_lang,
        style=Style(ButtonStyle.PRIMARY),
    ),
    Group(
        Button(
            GetText("admin-category-settings.show-with-no-items-btn"),
            id="show_with_no_items",
        ),
        Button(
            GetText("admin-category-settings.show-with-no-items-switcher-btn"),
            id="switch_with_no_items",
            on_click=on_switch_with_no_items,
        ),
        width=2,
    ),
    Cancel(
        GetText("inl-ui.back"),
    ),
    state=CategorySettingsState.settings,
    getter=settings_getter,
)

default_lang = Window(
    GetText("admin-category-default-lang"),
    Group(
        Select(
            GetTextSelect("admin-category-default-lang.btn"),
            id="select_lang",
            on_click=on_change_default_lang,  # type: ignore[arg-type]
            items="buttons",
            item_id_getter=lambda item: item.lang,
            type_factory=Language,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        state=CategorySettingsState.settings,
        id="back",
    ),
    state=CategorySettingsState.default_lang,
    getter=default_lang_getter,
)
