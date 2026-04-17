from uuid import UUID

from aiogram import F
from aiogram.enums import ButtonStyle
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Group, Select, SwitchTo
from aiogram_dialog.widgets.style import Style

from domain.product.position.item.enums import (
    ItemStatus,
)
from presentation.aiogram.state import StockItemState
from presentation.aiogram.widget import GetText, GetTextSelect, Pagination

from .callable import (
    on_add_item_text,
    on_archive_all,
    on_archive_item,
    on_delete_all,
    on_delete_item,
    on_filter_order,
    on_recover_item,
    on_select_item,
    on_select_item_status,
)
from .ctx import ITEMS_SCROLL
from .getter import (
    filters_getter,
    item_getter,
    items_getter,
)

items = Window(
    GetText("admin-position-warehouse-stock"),
    SwitchTo(
        GetText("admin-position-warehouse-stock.filters-btn"),
        id="to_filters",
        state=StockItemState.filters,
    ),
    Group(
        Select(
            GetTextSelect("admin-position-warehouse-stock.btn"),
            id="s_i",
            item_id_getter=lambda item: item.id,
            type_factory=UUID,
            on_click=on_select_item,  # type: ignore[arg-type]
            items="buttons",
        ),
        width=1,
    ),
    Pagination(scroll_id=ITEMS_SCROLL),
    Group(
        SwitchTo(
            GetText("inl-ui.archive-all"),
            state=StockItemState.archive_all_confirmation,
            id="to_archive_all_confirmation",
        ),
        SwitchTo(
            GetText("inl-ui.delete-all"),
            state=StockItemState.delete_all_confirmation,
            id="to_delete_all_confirmation",
        ),
        when=F["buttons"],
        width=2,
    ),
    SwitchTo(GetText("inl-ui.create"), id="to_add", state=StockItemState.add),
    Cancel(
        GetText("inl-ui.back"),
        id="back",
    ),
    state=StockItemState.items,
    getter=items_getter,
)

add = Window(
    GetText("admin-position-warehouse-add-stock"),
    TextInput(id="input_text", on_success=on_add_item_text),  # type: ignore[arg-type]
    SwitchTo(GetText("inl-ui.back"), id="back", state=StockItemState.items),
    state=StockItemState.add,
)

item = Window(
    GetText("admin-position-warehouse-item-stock"),
    SwitchTo(
        GetText("inl-ui.archive"),
        id="archive",
        state=StockItemState.archive_confirmation,
        when=F["item_status"] != ItemStatus.ARCHIVED,
    ),
    Button(GetText("inl-ui.recover"), id="recover", on_click=on_recover_item),
    SwitchTo(
        GetText("inl-ui.delete"),
        id="delete",
        state=StockItemState.delete_confirmation,
        when=F["item_status"] == ItemStatus.ARCHIVED,
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=StockItemState.items),
    state=StockItemState.item,
    getter=item_getter,
)

filters = Window(
    GetText("admin-position-warehouse-stock-filters"),
    Button(
        GetText("admin-position-warehouse-stock-filters.order-btn"),
        id="order",
        on_click=on_filter_order,
    ),
    Group(
        Select(
            GetTextSelect("admin-position-warehouse-stock-filters.status-btn"),
            items="buttons",
            item_id_getter=lambda i: i.item_status,
            type_factory=ItemStatus,
            on_click=on_select_item_status,  # type: ignore[arg-type]
            id="select_status",
        ),
        width=2,
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=StockItemState.items),
    state=StockItemState.filters,
    getter=filters_getter,
)

archive_confirmation = Window(
    GetText("admin-position-warehouse-archive-confirmation-stock"),
    SwitchTo(
        GetText("inl-ui.archive"),
        id="delete",
        on_click=on_archive_item,
        state=StockItemState.item,
        style=Style(ButtonStyle.DANGER),
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=StockItemState.item),
    state=StockItemState.archive_confirmation,
)


delete_confirmation = Window(
    GetText("admin-position-warehouse-delete-confirmation-stock"),
    SwitchTo(
        GetText("inl-ui.delete"),
        id="delete",
        on_click=on_delete_item,
        state=StockItemState.items,
        style=Style(ButtonStyle.DANGER),
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=StockItemState.item),
    state=StockItemState.delete_confirmation,
)

archive_all_confirmation = Window(
    GetText("admin-position-warehouse-archive-all-confirmation-stock"),
    SwitchTo(
        GetText("inl-ui.archive"),
        id="delete",
        on_click=on_archive_all,
        state=StockItemState.items,
        style=Style(ButtonStyle.DANGER),
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=StockItemState.items),
    state=StockItemState.archive_all_confirmation,
)


delete_all_confirmation = Window(
    GetText("admin-position-warehouse-delete-all-confirmation-stock"),
    SwitchTo(
        GetText("inl-ui.delete"),
        id="delete",
        on_click=on_delete_all,
        state=StockItemState.items,
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=StockItemState.items),
    state=StockItemState.delete_all_confirmation,
)
