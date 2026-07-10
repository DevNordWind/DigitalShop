from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Group, Select, SwitchTo, Url
from aiogram_dialog.widgets.text import Format

from aiogram import F
from app.domain.payment.enums import PaymentMethod
from app.presentation.aiogram.dialog.user.shopping.order.callable import (
    on_cancel,
    on_check,
    on_confirm_order_with_discount,
    on_input_coupon_code,
    on_pay_with_wallet,
    on_select_payment_method,
    on_to_order,
)
from app.presentation.aiogram.dialog.user.shopping.order.getter import (
    order_getter,
    payment_confirmed_getter,
    payment_getter,
    select_payment_method_getter,
)
from app.presentation.aiogram.state import OrderState
from app.presentation.aiogram.widget import GetText, GetTextSelect

order = Window(
    GetText("user-shopping-order"),
    SwitchTo(
        GetText("user-shopping-order.to-payment-btn"),
        id="to_select_payment_method",
        state=OrderState.select_payment_method,
        when=~F["can_confirm"],
    ),
    Button(
        GetText("inl-ui.confirm"),
        on_click=on_confirm_order_with_discount,  # type: ignore[bad-argument-type]
        id="confirm_with_discount",
        when=F["can_confirm"],
    ),
    SwitchTo(
        GetText("user-shopping-order.coupon-btn"),
        id="to_input_coupon_code",
        state=OrderState.input_coupon_code,
    ),
    Button(
        GetText("user-shopping-order.cancel-btn"),
        id="cancel",
        on_click=on_cancel,  # type: ignore[bad-argument-type]
    ),
    state=OrderState.order,
    getter=order_getter,
)

input_coupon_code = Window(
    GetText("user-shopping-order-coupon-code"),
    TextInput(on_success=on_input_coupon_code, id="indput_coupon_code"),
    SwitchTo(GetText("inl-ui.back"), id="back", state=OrderState.order),
    state=OrderState.input_coupon_code,
)


select_payment_method = Window(
    GetText("user-shopping-order-select-payment"),
    Button(
        GetText("user-shopping-order-select-payment.wallet-btn"),
        id="pay_with_wallet",
        on_click=on_pay_with_wallet,  # type: ignore[bad-argument-type]
    ),
    Group(
        Select(
            GetTextSelect("user-shopping-order-select-payment.payment-btn"),
            items="buttons",
            id="sel_method",
            type_factory=PaymentMethod,
            on_click=on_select_payment_method,  # type: ignore[arg-type]
            item_id_getter=lambda item: item.method,
        ),
        width=2,
    ),
    SwitchTo(GetText("inl-ui.back"), state=OrderState.order, id="back"),
    state=OrderState.select_payment_method,
    getter=select_payment_method_getter,
)


payment = Window(
    GetText("user-shopping-order-payment"),
    Url(
        text=GetText("user-shopping-order-payment.pay-btn"),
        url=Format("{pay_url}"),
        id="pay",
    ),
    Button(
        GetText("user-shopping-order-payment.check-btn"),
        id="check",
        on_click=on_check,  # type: ignore[bad-argument-type]
    ),
    Button(
        GetText("user-shopping-order-payment.cancel-btn"),
        id="cancel",
        on_click=on_cancel,  # type: ignore[bad-argument-type]
    ),
    getter=payment_getter,
    state=OrderState.payment,
)

payment_confirmed = Window(
    Format("{text}"),
    Button(Format("{to_order_text}"), id="to_order", on_click=on_to_order),
    Cancel(Format("{cancel_text}")),
    getter=payment_confirmed_getter,
    state=OrderState.payment_confirmed,
)
