from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    Select,
    SwitchTo,
    Url,
)
from aiogram_dialog.widgets.text import Format

from domain.payment.enums import PaymentMethod
from presentation.aiogram.dialog.error import on_decimal_error
from presentation.aiogram.dialog.user.wallet.top_up.callable import (
    on_cancel,
    on_check,
    on_input_amount,
    on_select_currency,
    on_select_payment_method,
)
from presentation.aiogram.dialog.user.wallet.top_up.getter import (
    input_amount_getter,
    payment_getter,
    select_currency_getter,
    select_payment_method_getter,
)
from presentation.aiogram.mapper.decimal import map_decimal
from presentation.aiogram.state import TopUpState
from presentation.aiogram.widget import GetText, GetTextSelect

input_amount = Window(
    GetText("top-up-input-amount"),
    TextInput(
        on_success=on_input_amount,
        on_error=on_decimal_error,
        type_factory=map_decimal,
        id="input_amount",
    ),
    SwitchTo(
        GetText("top-up-input-amount.another-wallet-btn"),
        id="another_wallet",
        state=TopUpState.select_currency,
    ),
    Cancel(GetText("inl-ui.back")),
    state=TopUpState.input_amount,
    getter=input_amount_getter,
)

select_currency = Window(
    GetText("top-up-select-currency"),
    Group(
        Select(
            GetTextSelect("top-up-select-currency.btn"),
            id="select_currency",
            item_id_getter=lambda item: item.currency,
            items="buttons",
            on_click=on_select_currency,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=TopUpState.input_amount),
    state=TopUpState.select_currency,
    getter=select_currency_getter,
)

select_payment_method = Window(
    GetText("top-up-select-payment-method"),
    Group(
        Select(
            GetTextSelect("top-up-select-payment-method.btn"),
            id="select_method",
            on_click=on_select_payment_method,  # type: ignore[arg-type]
            items="buttons",
            type_factory=PaymentMethod,
            item_id_getter=lambda item: item.method,
        ),
        width=2,
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=TopUpState.input_amount),
    state=TopUpState.select_payment_method,
    getter=select_payment_method_getter,
)

payment = Window(
    GetText("top-up-payment"),
    Url(
        text=GetText("top-up-payment.pay-btn"),
        url=Format("{invoice_url}"),
        id="pay_btn",
    ),
    Button(
        GetText("top-up-payment.check-btn"),
        id="check",
        on_click=on_check,
    ),
    Button(
        GetText("top-up-payment.cancel-btn"),
        on_click=on_cancel,
        id="cancel",
    ),
    state=TopUpState.payment,
    getter=payment_getter,
)
