from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    Select,
    Start,
    SwitchTo,
)

from domain.common.money import Currency
from domain.user.enums import UserRole
from presentation.aiogram.dialog.error import on_decimal_error
from presentation.aiogram.mapper.decimal import map_decimal
from presentation.aiogram.state import BroadcastState, UsersManagementState
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import (
    on_demote_to_user,
    on_input_top_amount,
    on_input_user_identifier,
    on_promote_to_admin,
    on_select_top_up_currency,
    on_start_orders,
)
from .getter import input_top_up_amount_getter, user_getter

users = Window(
    GetText("users-management"),
    Start(
        GetText("users-management.broadcast-btn"),
        state=BroadcastState.broadcast,
        id="start_broadcast",
    ),
    SwitchTo(
        GetText("users-management.find-btn"),
        id="to_find",
        state=UsersManagementState.find,
    ),
    Cancel(GetText("inl-ui.back")),
    state=UsersManagementState.users,
)

find = Window(
    GetText("users-management-find"),
    TextInput(on_success=on_input_user_identifier, id="input_user_identifier"),
    SwitchTo(
        GetText("inl-ui.back"), id="back", state=UsersManagementState.users
    ),
    state=UsersManagementState.find,
)

user = Window(
    GetText("users-management-user"),
    Button(
        GetText("users-management-user.promote-to-admin-btn"),
        id="promote_to_admin",
        on_click=on_promote_to_admin,
        when=(F["role"] == UserRole.USER)
        & (F["user_role"] >= UserRole.SUPER_ADMIN),
    ),
    Button(
        GetText("users-management-user.demote-to-user-btn"),
        id="demote_to_user",
        on_click=on_demote_to_user,
        when=(F["role"] == UserRole.ADMIN)
        & (F["user_role"] >= UserRole.SUPER_ADMIN),
    ),
    SwitchTo(
        GetText("users-management-user.top-up-btn"),
        id="top_up",
        state=UsersManagementState.input_top_up_amount,
    ),
    Button(
        GetText("users-management-user.orders-btn"),
        id="start_orders",
        on_click=on_start_orders,
    ),
    SwitchTo(
        GetText("inl-ui.back"), id="back", state=UsersManagementState.find
    ),
    getter=user_getter,
    state=UsersManagementState.user,
)

input_top_up_amount = Window(
    GetText("users-management-top-up"),
    Group(
        Select(
            GetTextSelect("users-management-top-up.btn"),
            id="select_currency",
            on_click=on_select_top_up_currency,  # type: ignore[arg-type]
            items="buttons",
            type_factory=Currency,
            item_id_getter=lambda item: item.currency,
        )
    ),
    TextInput(
        on_success=on_input_top_amount,
        on_error=on_decimal_error,
        type_factory=map_decimal,
        id="input_top_amount",
    ),
    SwitchTo(
        GetText("inl-ui.back"), id="back", state=UsersManagementState.user
    ),
    state=UsersManagementState.input_top_up_amount,
    getter=input_top_up_amount_getter,
)
