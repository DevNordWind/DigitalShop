from datetime import datetime
from decimal import Decimal

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    Select,
    SwitchTo,
)

from domain.common.money import Currency
from domain.coupon.enums import CouponType
from presentation.aiogram.dialog.error import on_decimal_error
from presentation.aiogram.mapper.decimal import map_decimal
from presentation.aiogram.state import CreateCouponState
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import (
    on_clear_amount,
    on_confirm,
    on_convert_to_other,
    on_date_error,
    on_input_amount,
    on_input_code,
    on_input_percent,
    on_input_valid_from,
    on_input_valid_until,
    on_select_currency,
    on_select_type,
)
from .getter import (
    input_amount_getter,
    input_code_getter,
    select_type_getter,
    view_getter,
)

view = Window(
    GetText("admin-coupon-create-view"),
    Group(
        SwitchTo(
            GetText("admin-coupon-create-view.code-btn"),
            id="to_code",
            state=CreateCouponState.input_code,
        ),
        SwitchTo(
            GetText("admin-coupon-create-view.type-btn"),
            state=CreateCouponState.select_type,
            id="to_type",
        ),
        width=2,
    ),
    SwitchTo(
        GetText("admin-coupon-create-view.valid-from-btn"),
        id="valid_from",
        state=CreateCouponState.input_valid_from,
    ),
    SwitchTo(
        GetText("admin-coupon-create-view.valid-until-btn"),
        id="valid_until",
        state=CreateCouponState.input_valid_until,
    ),
    Button(
        GetText("inl-ui.confirm"),
        id="confirm",
        when=F["can_create"],
        on_click=on_confirm,
    ),
    Cancel(GetText("inl-ui.back")),
    state=CreateCouponState.view,
    getter=view_getter,
)

input_code = Window(
    GetText("admin-coupon-create-code"),
    TextInput(id="input_code", on_success=on_input_code),
    SwitchTo(GetText("inl-ui.back"), id="back", state=CreateCouponState.view),
    getter=input_code_getter,
    state=CreateCouponState.input_code,
)

select_type = Window(
    GetText("admin-coupon-create-type"),
    Group(
        Select(
            GetTextSelect("admin-coupon-create-type.btn"),
            id="select_type",
            items="buttons",
            item_id_getter=lambda item: item.type,
            type_factory=CouponType,
            on_click=on_select_type,
        ),
        width=1,
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=CreateCouponState.view),
    state=CreateCouponState.select_type,
    getter=select_type_getter,
)

input_percent = Window(
    GetText("admin-coupon-create-coefficient"),
    TextInput[Decimal](
        on_success=on_input_percent,
        on_error=on_decimal_error,
        type_factory=map_decimal,
        id="input_percent",
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=CreateCouponState.view),
    state=CreateCouponState.input_percent,
)

input_amount = Window(
    GetText("admin-coupon-create-fixed"),
    Group(
        Select(
            GetTextSelect("admin-coupon-create-fixed.btn"),
            id="select_currency",
            items="buttons",
            item_id_getter=lambda item: item.currency,
            on_click=on_select_currency,  # type: ignore[arg-type]
            type_factory=Currency,
        ),
        width=2,
    ),
    TextInput[Decimal](
        on_success=on_input_amount,
        on_error=on_decimal_error,
        type_factory=map_decimal,
        id="input_amount",
    ),
    Button(
        GetText("admin-coupon-create-fixed.convert-btn"),
        id="convert",
        when=F["can_convert_to_other"],
        on_click=on_convert_to_other,
    ),
    Button(
        GetText("inl-ui.clear"),
        when=F["can_clear"],
        on_click=on_clear_amount,
        id="clear",
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=CreateCouponState.view),
    state=CreateCouponState.input_amount,
    getter=input_amount_getter,
)

input_valid_from = Window(
    GetText("admin-coupon-create-valid-from"),
    TextInput(
        id="input_validity",
        on_error=on_date_error,
        on_success=on_input_valid_from,
        type_factory=lambda value: datetime.strptime(
            value,
            "%d.%m.%y %H:%M",
        ).astimezone(),
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=CreateCouponState.view),
    state=CreateCouponState.input_valid_from,
)
input_valid_until = Window(
    GetText("admin-coupon-create-valid-until"),
    TextInput(
        id="input_validity",
        on_error=on_date_error,
        on_success=on_input_valid_until,
        type_factory=lambda value: datetime.strptime(
            value,
            "%d.%m.%y %H:%M",
        ).astimezone(),
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=CreateCouponState.view),
    state=CreateCouponState.input_valid_until,
)
