from uuid import UUID

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Group, Select, SwitchTo

from domain.order.enums import OrderStatus
from presentation.aiogram.dialog.user.profile.order.callable import (
    on_order_status,
    on_select_order,
    on_sorting_order,
    on_upload_items,
)
from presentation.aiogram.dialog.user.profile.order.ctx import ORDER_SCROLL
from presentation.aiogram.dialog.user.profile.order.getter import (
    filters_getter,
    order_getter,
    orders_getter,
)
from presentation.aiogram.state import OrdersState
from presentation.aiogram.widget import GetText, GetTextSelect, Pagination

orders = Window(
    GetText("user-orders"),
    SwitchTo(
        GetText("user-orders.filters-btn"),
        id="to_filters",
        state=OrdersState.filters,
    ),
    Group(
        Select(
            GetTextSelect("user-orders.btn"),
            id="s_o",
            items="buttons",
            type_factory=UUID,
            item_id_getter=lambda item: item.id,
            on_click=on_select_order,  # type: ignore[arg-type]
        ),
        width=1,
    ),
    Pagination(scroll_id=ORDER_SCROLL),
    Cancel(GetText("inl-ui.back")),
    state=OrdersState.orders,
    getter=orders_getter,
)

filters = Window(
    GetText("user-orders-filters"),
    Button(
        GetText("user-orders-filters.order-btn"),
        id="sorting_order",
        on_click=on_sorting_order,
    ),
    Group(
        Select(
            GetTextSelect("user-orders-filters.status-btn"),
            id="select_status",
            type_factory=OrderStatus,
            item_id_getter=lambda item: item.status,
            items="buttons",
            on_click=on_order_status,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=OrdersState.orders),
    state=OrdersState.filters,
    getter=filters_getter,
)


order = Window(
    GetText("user-order"),
    Button(
        GetText("user-order.upload-items"),
        id="upload_items",
        when=F["can_view_items"],
        on_click=on_upload_items,
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=OrdersState.orders),
    state=OrdersState.order,
    getter=order_getter,
)
