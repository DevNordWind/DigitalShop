from uuid import UUID

from aiogram import F
from aiogram.enums import ButtonStyle
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Group, Select, SwitchTo
from aiogram_dialog.widgets.style import Style

from presentation.aiogram.dialog.admin.position.fixed_item.callable import (
    on_add_item_text,
    on_archive_item,
    on_delete_archived_item,
    on_recover_archived_item,
    on_replace_item_text,
    on_select_archived_item,
)
from presentation.aiogram.dialog.admin.position.fixed_item.ctx import (
    ARCHIVED_ITEMS_SCROLL_ID,
)
from presentation.aiogram.dialog.admin.position.fixed_item.getter import (
    archive_getter,
    archived_item_getter,
    item_getter,
)
from presentation.aiogram.state import FixedItemState
from presentation.aiogram.widget import GetText, GetTextSelect, Pagination

item = Window(
    GetText("admin-position-warehouse-fixed"),
    SwitchTo(
        GetText("admin-position-warehouse-fixed.replace-btn"),
        id="to_replace",
        state=FixedItemState.replace,
        when=(F["has_item"]) & (~F["is_archived"]),
    ),
    SwitchTo(
        GetText("admin-position-warehouse-fixed.archive-btn"),
        id="to_archive",
        state=FixedItemState.archive,
    ),
    SwitchTo(
        GetText("inl-ui.archive"),
        id="to_archive_confirmation",
        when=(~F["is_archived"]) & (F["has_item"]),
        state=FixedItemState.archive_confirmation,
    ),
    SwitchTo(
        GetText("inl-ui.delete"),
        id="to_delete_confirmation",
        when=F["is_archived"],
        state=FixedItemState.delete_confirmation,
    ),
    SwitchTo(
        GetText("inl-ui.create"),
        state=FixedItemState.add,
        id="to_add",
        when=(~F["has_item"]) | (F["is_archived"]),
    ),
    Cancel(
        GetText("inl-ui.back"),
    ),
    state=FixedItemState.item,
    getter=item_getter,
)

replace = Window(
    GetText("admin-position-warehouse-replace-fixed"),
    TextInput(
        id="input_text",
        type_factory=str,
        on_success=on_replace_item_text,  # type: ignore[arg-type]
    ),
    SwitchTo(GetText("inl-ui.back"), state=FixedItemState.item, id="back"),
    state=FixedItemState.replace,
)

add = Window(
    GetText("admin-position-warehouse-add-fixed"),
    TextInput(id="input_text", type_factory=str, on_success=on_add_item_text),  # type: ignore[arg-type]
    SwitchTo(GetText("inl-ui.back"), state=FixedItemState.item, id="back"),
    state=FixedItemState.add,
)

archive = Window(
    GetText("admin-position-warehouse-archive-fixed"),
    Group(
        Select(
            GetTextSelect("admin-position-warehouse-archive-fixed.btn"),
            id="s_a_i",
            items="buttons",
            type_factory=UUID,
            on_click=on_select_archived_item,  # type: ignore[arg-type]
            item_id_getter=lambda item: item.id,
        ),
        width=1,
    ),
    Pagination(scroll_id=ARCHIVED_ITEMS_SCROLL_ID),
    SwitchTo(GetText("inl-ui.back"), id="back", state=FixedItemState.item),
    state=FixedItemState.archive,
    getter=archive_getter,
)

archived_item = Window(
    GetText("admin-position-warehouse-archived-item-fixed"),
    SwitchTo(
        GetText("inl-ui.delete"),
        id="delete",
        state=FixedItemState.delete_confirmation,
    ),
    SwitchTo(
        GetText("inl-ui.recover"),
        id="recover",
        on_click=on_recover_archived_item,
        state=FixedItemState.item,
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=FixedItemState.archive),
    state=FixedItemState.archived_item,
    getter=archived_item_getter,
)

archive_confirmation = Window(
    GetText("admin-position-warehouse-archive-confirmation-fixed"),
    SwitchTo(
        GetText("inl-ui.archive"),
        on_click=on_archive_item,
        id="archive",
        state=FixedItemState.item,
        style=Style(ButtonStyle.DANGER),
    ),
    SwitchTo(GetText("inl-ui.back"), state=FixedItemState.item, id="back"),
    state=FixedItemState.archive_confirmation,
)

delete_confirmation = Window(
    GetText("admin-position-warehouse-delete-confirmation-fixed"),
    SwitchTo(
        GetText("inl-ui.delete"),
        on_click=on_delete_archived_item,
        id="delete",
        state=FixedItemState.item,
        style=Style(ButtonStyle.DANGER),
    ),
    SwitchTo(GetText("inl-ui.back"), state=FixedItemState.item, id="back"),
    state=FixedItemState.delete_confirmation,
)
