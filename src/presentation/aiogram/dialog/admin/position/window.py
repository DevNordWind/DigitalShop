from uuid import UUID

from aiogram import F
from aiogram.enums import ButtonStyle
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    NumberedPager,
    Select,
    Start,
    StubScroll,
    SwitchTo,
)
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.style import Style

from domain.common.localized import Language
from domain.product.category.enums import CategoryStatus
from domain.product.position.enums import PositionStatus
from presentation.aiogram.state import (
    AdminPositionState,
    PositionSettingsState,
)
from presentation.aiogram.widget import GetText, GetTextSelect, Pagination

from .callable import (
    on_archive_all_positions,
    on_archive_position,
    on_category_sorting_order,
    on_category_status,
    on_create,
    on_delete_all_positions,
    on_delete_position,
    on_edit_description,
    on_edit_item,
    on_edit_media,
    on_edit_name,
    on_edit_price,
    on_position_back,
    on_position_sorting_order,
    on_position_status,
    on_recover_position,
    on_select_category,
    on_select_lang,
    on_select_position,
)
from .ctx import CATEGORIES_SCROLL, POSITION_MEDIA_SCROLL, POSITIONS_SCROLL
from .getter import (
    archive_confirmation_getter,
    category_filters_getter,
    delete_confirmation_getter,
    position_filters_getter,
    position_getter,
    select_category_getter,
    select_position_getter,
)

select_category = Window(
    GetText("admin-positions-categories"),
    SwitchTo(
        GetText("admin-positions-categories.filters-btn"),
        id="to_filters",
        state=AdminPositionState.category_filters,
    ),
    Group(
        Select(
            GetTextSelect("admin-positions-categories.btn"),
            id="s_c",
            type_factory=UUID,
            items="buttons",
            on_click=on_select_category,  # type: ignore[arg-type]
            item_id_getter=lambda item: item.id,
        ),
        width=1,
    ),
    Pagination(scroll_id=CATEGORIES_SCROLL),
    Start(
        GetText("admin-positions-categories.settings-btn"),
        id="to_settings",
        state=PositionSettingsState.settings,
    ),
    Cancel(GetText("inl-ui.back")),
    state=AdminPositionState.select_category,
    getter=select_category_getter,
)

category_filters = Window(
    GetText("admin-positions-category-filters"),
    Button(
        GetText("admin-positions-category-filters.order-btn"),
        id="order",
        on_click=on_category_sorting_order,
    ),
    Group(
        Select(
            GetTextSelect("admin-positions-category-filters.status-btn"),
            items="buttons",
            type_factory=CategoryStatus,
            on_click=on_category_status,  # type: ignore[arg-type]
            id="select_status",
            item_id_getter=lambda item: item.status,
        ),
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminPositionState.select_category,
    ),
    getter=category_filters_getter,
    state=AdminPositionState.category_filters,
)

select_position = Window(
    GetText("admin-positions"),
    SwitchTo(
        GetText("admin-positions.filters-btn"),
        id="to_filters",
        state=AdminPositionState.position_filters,
    ),
    Group(
        Select(
            GetTextSelect("admin-positions.btn"),
            id="s_c",
            type_factory=UUID,
            items="buttons",
            item_id_getter=lambda item: item.id,
            on_click=on_select_position,  # type: ignore[arg-type]
        ),
        width=1,
    ),
    Pagination(scroll_id=POSITIONS_SCROLL),
    Group(
        SwitchTo(
            GetText("inl-ui.archive-all"),
            id="to_archive_all_confirmation",
            state=AdminPositionState.archive_all_confirmation,
        ),
        SwitchTo(
            GetText("inl-ui.delete-all"),
            id="to_delete_all_confirmation",
            state=AdminPositionState.delete_all_confirmation,
        ),
        width=2,
        when=F["buttons"],
    ),
    Start(
        GetText("admin-positions.settings-btn"),
        id="to_settings",
        state=PositionSettingsState.settings,
    ),
    Button(GetText("inl-ui.create"), id="create_btn", on_click=on_create),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminPositionState.select_category,
    ),
    state=AdminPositionState.select_position,
    getter=select_position_getter,
)

position_filters = Window(
    GetText("admins-position-filters"),
    Button(
        GetText("admins-position-filters.order-btn"),
        id="order",
        on_click=on_position_sorting_order,
    ),
    Group(
        Select(
            GetTextSelect("admins-position-filters.status-btn"),
            items="buttons",
            type_factory=PositionStatus,
            on_click=on_position_status,  # type: ignore[arg-type]
            id="select_status",
            item_id_getter=lambda item: item.status,
        ),
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminPositionState.select_position,
    ),
    getter=position_filters_getter,
    state=AdminPositionState.position_filters,
)

position = Window(
    GetText("admin-position"),
    DynamicMedia(selector="media", when=F["media"]),
    StubScroll(id=POSITION_MEDIA_SCROLL, pages="pages"),
    NumberedPager(scroll=POSITION_MEDIA_SCROLL, when=F["pages"] > 1),
    Button(GetText("admin-position.show-language-btn"), id="show_language"),
    Group(
        Select(
            GetTextSelect("admin-position.lang-btn"),
            id="select_lang",
            items="buttons",
            item_id_getter=lambda item: item.lang,
            type_factory=Language,
            on_click=on_select_lang,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    Button(
        GetText("admin-position.name-btn"),
        id="to_edit_name",
        on_click=on_edit_name,
        when=~F["is_archived"],
    ),
    Button(
        GetText("admin-position.description-btn"),
        id="to_edit_description",
        on_click=on_edit_description,
        when=~F["is_archived"],
    ),
    Group(
        Button(
            GetText("admin-position.media-btn"),
            id="to_edit_media",
            on_click=on_edit_media,
            when=~F["is_archived"],
        ),
        Button(
            GetText("admin-position.price-btn"),
            id="to_price_name",
            on_click=on_edit_price,
            when=~F["is_archived"],
        ),
        width=2,
    ),
    Button(
        GetText("admin-position.items-btn"),
        id="to_edit_items",
        on_click=on_edit_item,
        when=~F["is_archived"],
    ),
    SwitchTo(
        GetText("inl-ui.archive"),
        id="to_archive_confirmation",
        state=AdminPositionState.archive_confirmation,
        when=~F["is_archived"],
    ),
    Button(
        GetText("inl-ui.recover"),
        id="recover",
        when=F["is_archived"],
        on_click=on_recover_position,
    ),
    SwitchTo(
        GetText("inl-ui.delete"),
        id="to_delete_confirmation",
        when=F["is_archived"],
        state=AdminPositionState.delete_confirmation,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminPositionState.select_position,
        on_click=on_position_back,
    ),
    getter=position_getter,
    state=AdminPositionState.position,
)

archive_confirmation = Window(
    GetText("admin-position-archive-confirmation"),
    Button(
        GetText("inl-ui.archive"),
        style=Style(ButtonStyle.DANGER),
        on_click=on_archive_position,
        id="archive",
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminPositionState.position,
    ),
    state=AdminPositionState.archive_confirmation,
    getter=archive_confirmation_getter,
)

delete_confirmation = Window(
    GetText("admin-position-delete-confirmation"),
    Button(
        GetText("inl-ui.delete"),
        style=Style(ButtonStyle.DANGER),
        on_click=on_delete_position,
        id="delete",
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminPositionState.position,
    ),
    state=AdminPositionState.delete_confirmation,
    getter=delete_confirmation_getter,
)

archive_all_confirmation = Window(
    GetText("admin-position-archive-all-confirmation"),
    SwitchTo(
        GetText("inl-ui.archive"),
        style=Style(ButtonStyle.DANGER),
        on_click=on_archive_all_positions,
        id="archive",
        state=AdminPositionState.select_position,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminPositionState.select_position,
    ),
    state=AdminPositionState.archive_all_confirmation,
)

delete_all_confirmation = Window(
    GetText("admin-position-delete-all-confirmation"),
    SwitchTo(
        GetText("inl-ui.delete"),
        style=Style(ButtonStyle.DANGER),
        on_click=on_delete_all_positions,
        id="delete",
        state=AdminPositionState.select_position,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminPositionState.select_position,
    ),
    state=AdminPositionState.delete_all_confirmation,
)
