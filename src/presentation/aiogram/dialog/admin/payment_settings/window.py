from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Group, Select, SwitchTo

from domain.payment.enums import CommissionType, PaymentMethod
from presentation.aiogram.dialog.error import on_decimal_error
from presentation.aiogram.mapper.decimal import map_decimal
from presentation.aiogram.state.admin import PaymentSettingsState
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import (
    on_change_commission,
    on_input_commission,
    on_select_payment_method,
    on_switch_status,
)
from .getter import select_method_getter, setting_getter

select_method = Window(
    GetText("admin-payment-methods"),
    Group(
        Select(
            GetTextSelect("admin-payment-methods.btn"),
            id="select_method",
            item_id_getter=lambda item: item.method,
            items="buttons",
            on_click=on_select_payment_method,  # type: ignore[arg-type]
            type_factory=PaymentMethod,
        ),
        width=2,
    ),
    Cancel(GetText("inl-ui.back")),
    state=PaymentSettingsState.select_method,
    getter=select_method_getter,
)

setting = Window(
    GetText("admin-payment-settings"),
    Button(GetText("admin-payment-settings.commission-btn"), id="commission"),
    Group(
        Select(
            GetTextSelect("admin-payment-settings.commission-type-btn"),
            id="select_type",
            items="buttons",
            on_click=on_change_commission,  # type: ignore[arg-type]
            type_factory=CommissionType,
            item_id_getter=lambda item: item.type,
        ),
        width=2,
    ),
    Group(
        Button(GetText("admin-payment-settings.status-btn"), id="status"),
        Button(
            GetText("admin-payment-settings.switch-status-btn"),
            id="switch_status",
            on_click=on_switch_status,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=PaymentSettingsState.select_method,
    ),
    state=PaymentSettingsState.setting,
    getter=setting_getter,
)

input_commission = Window(
    GetText("admin-payment-settings-commission"),
    TextInput(
        type_factory=map_decimal,
        on_success=on_input_commission,
        on_error=on_decimal_error,
        id="input_commission",
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=PaymentSettingsState.setting,
    ),
    state=PaymentSettingsState.input_commission,
)
