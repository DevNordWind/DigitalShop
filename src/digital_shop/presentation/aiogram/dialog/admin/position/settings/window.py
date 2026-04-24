from aiogram.enums import ButtonStyle
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    Select,
    SwitchTo,
)
from aiogram_dialog.widgets.style import Style
from domain.common.localized import Language
from domain.common.money import Currency
from presentation.aiogram.state import (
    PositionSettingsState,
)
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import (
    on_change_default_currency,
    on_change_default_lang,
    on_switch_with_no_items,
)
from .getter import (
    default_currency_getter,
    default_lang_getter,
    settings_getter,
)

settings = Window(
    GetText("admin-position-settings"),
    SwitchTo(
        GetText("admin-position-settings.default-lang-btn"),
        id="to_default_lang",
        state=PositionSettingsState.default_lang,
        style=Style(ButtonStyle.PRIMARY),
    ),
    SwitchTo(
        GetText("admin-position-settings.default-currency-btn"),
        id="to_default_currency",
        state=PositionSettingsState.default_currency,
        style=Style(ButtonStyle.PRIMARY),
    ),
    Group(
        Button(
            GetText("admin-position-settings.show-with-no-items-btn"),
            id="show_with_no_items",
        ),
        Button(
            GetText("admin-position-settings.show-with-no-items-switcher-btn"),
            id="switch_with_no_items",
            on_click=on_switch_with_no_items,
        ),
        width=2,
    ),
    Cancel(GetText("inl-ui.back")),
    getter=settings_getter,
    state=PositionSettingsState.settings,
)

default_lang = Window(
    GetText("admin-position-default-lang"),
    Group(
        Select(
            GetTextSelect("admin-position-default-lang.btn"),
            id="select_lang",
            on_click=on_change_default_lang,  # type: ignore[arg-type]
            items="buttons",
            type_factory=Language,
            item_id_getter=lambda item: item.lang,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=PositionSettingsState.settings,
    ),
    getter=default_lang_getter,
    state=PositionSettingsState.default_lang,
)

default_currency = Window(
    GetText("admin-position-default-currency"),
    Group(
        Select(
            GetTextSelect("admin-position-default-currency.btn"),
            id="select_currency",
            on_click=on_change_default_currency,  # type: ignore[arg-type]
            items="buttons",
            type_factory=Currency,
            item_id_getter=lambda item: item.currency,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=PositionSettingsState.settings,
    ),
    getter=default_currency_getter,
    state=PositionSettingsState.default_currency,
)
