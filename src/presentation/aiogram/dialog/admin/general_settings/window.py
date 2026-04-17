from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, SwitchTo

from presentation.aiogram.dialog.error import on_decimal_error
from presentation.aiogram.mapper.decimal import map_decimal
from presentation.aiogram.state.admin import GeneralSettingsState
from presentation.aiogram.widget import GetText

from .callable import (
    on_input_referral_percent,
    on_input_support_contact,
    on_switch_tech_work_status,
)
from .getter import general_settings_getter

general_settings = Window(
    GetText("admin-general-settings"),
    Button(
        GetText("admin-general-settings.tech-work-btn"),
        id="tech_work_switcher",
        on_click=on_switch_tech_work_status,
    ),
    SwitchTo(
        GetText("admin-general-settings.support-contact-btn"),
        id="to_input_support_contact",
        state=GeneralSettingsState.input_support_contact,
    ),
    SwitchTo(
        GetText("admin-general-settings.referral-percent-btn"),
        id="to_input_referral_percent",
        state=GeneralSettingsState.input_referral_percent,
    ),
    Cancel(GetText("inl-ui.back")),
    getter=general_settings_getter,
    state=GeneralSettingsState.general_settings,
)

input_support_contact = Window(
    GetText("admin-general-settings-support"),
    TextInput(on_success=on_input_support_contact, id="input_contact"),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=GeneralSettingsState.general_settings,
    ),
    state=GeneralSettingsState.input_support_contact,
)

input_referral_percent = Window(
    GetText("admin-general-settings-referral-percent"),
    TextInput(
        on_success=on_input_referral_percent,
        id="input_contact",
        on_error=on_decimal_error,
        type_factory=map_decimal,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=GeneralSettingsState.general_settings,
    ),
    state=GeneralSettingsState.input_referral_percent,
)
