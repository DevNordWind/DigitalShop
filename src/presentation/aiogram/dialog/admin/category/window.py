from uuid import UUID

from aiogram import F
from aiogram.enums import ButtonStyle
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    Select,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.style import Style

from domain.common.localized import Language
from domain.product.category.enums import CategoryStatus
from presentation.aiogram.dialog.admin.category.const import (
    CATEGORIES_SCROLL,
)
from presentation.aiogram.state import (
    AdminCategoryState,
    CategorySettingsState,
    CreateCategoryState,
)
from presentation.aiogram.widget import GetText, GetTextSelect, Pagination

from .callable import (
    on_archive_all_categories,
    on_archive_category,
    on_category_status,
    on_delete_all_categories,
    on_delete_category,
    on_edit_description,
    on_edit_media,
    on_edit_name,
    on_recover_category,
    on_select_category,
    on_select_lang,
    on_sorting_order,
)
from .getter import (
    archive_confirmation_getter,
    categories_getter,
    category_getter,
    delete_confirmation_getter,
    filters_getter,
)

categories = Window(
    GetText("admin-categories"),
    SwitchTo(
        GetText("admin-categories.filters-btn"),
        id="to_filters",
        state=AdminCategoryState.filters,
    ),
    Group(
        Select(
            GetTextSelect("admin-categories.btn"),
            id="s_c",
            item_id_getter=lambda item: item.id,
            items="buttons",
            type_factory=UUID,
            on_click=on_select_category,  # type: ignore[arg-type]
        ),
        width=1,
    ),
    Pagination(scroll_id=CATEGORIES_SCROLL),
    Group(
        SwitchTo(
            GetText("inl-ui.archive-all"),
            id="to_archive_all_confirmation",
            state=AdminCategoryState.archive_all_confirmation,
        ),
        SwitchTo(
            GetText("inl-ui.delete-all"),
            id="to_delete_all_confirmation",
            state=AdminCategoryState.delete_all_confirmation,
        ),
        width=2,
        when=F["buttons"],
    ),
    Start(
        GetText("admin-categories.settings-btn"),
        id="to_settings",
        state=CategorySettingsState.settings,
    ),
    Start(
        GetText("inl-ui.create"),
        id="to_create",
        state=CreateCategoryState.view,
    ),
    Cancel(GetText("inl-ui.back")),
    state=AdminCategoryState.categories,
    getter=categories_getter,
)

filters = Window(
    GetText("admins-category-filters"),
    Button(
        GetText("admins-category-filters.order-btn"),
        id="sorting_order",
        on_click=on_sorting_order,
    ),
    Group(
        Select(
            GetTextSelect("admins-category-filters.status-btn"),
            id="select_status",
            type_factory=CategoryStatus,
            items="buttons",
            item_id_getter=lambda item: item.status,
            on_click=on_category_status,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminCategoryState.categories,
    ),
    state=AdminCategoryState.filters,
    getter=filters_getter,
)


category = Window(
    GetText("admin-category"),
    DynamicMedia(selector="media", when=F["media"]),
    Button(
        GetText("admin-category.show-language-btn"),
        id="show_language",
    ),
    Group(
        Select(
            GetTextSelect("admin-category.lang-btn"),
            items="buttons",
            item_id_getter=lambda item: item.lang,
            type_factory=Language,
            id="select_lang",
            on_click=on_select_lang,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    Group(
        Button(
            GetText("admin-category.name-btn"),
            id="to_name",
            on_click=on_edit_name,
        ),
        Button(
            GetText("admin-category.description-btn"),
            id="to_description",
            on_click=on_edit_description,
        ),
        width=2,
        when=~F["is_archived"],
    ),
    Button(
        GetText("admin-category.media-btn"),
        id="to_media",
        on_click=on_edit_media,
        when=~F["is_archived"],
    ),
    Button(
        GetText("inl-ui.recover"),
        id="recover",
        on_click=on_recover_category,
        when=F["is_archived"],
    ),
    SwitchTo(
        GetText("inl-ui.delete"),
        id="to_delete_confirmation",
        state=AdminCategoryState.delete_confirmation,
        when=F["is_archived"],
    ),
    SwitchTo(
        GetText("inl-ui.archive"),
        id="to_archive_confirmation",
        state=AdminCategoryState.archive_confirmation,
        when=~F["is_archived"],
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminCategoryState.categories,
    ),
    state=AdminCategoryState.category,
    getter=category_getter,
)

archive_confirmation = Window(
    GetText("admin-category-archive-confirmation"),
    SwitchTo(
        GetText("inl-ui.archive"),
        id="archive",
        on_click=on_archive_category,
        style=Style(ButtonStyle.DANGER),
        state=AdminCategoryState.category,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminCategoryState.category,
    ),
    state=AdminCategoryState.archive_confirmation,
    getter=archive_confirmation_getter,
)

delete_confirmation = Window(
    GetText("admin-category-delete-confirmation"),
    SwitchTo(
        GetText("inl-ui.delete"),
        id="delete",
        on_click=on_delete_category,
        style=Style(ButtonStyle.DANGER),
        state=AdminCategoryState.categories,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminCategoryState.category,
    ),
    state=AdminCategoryState.delete_confirmation,
    getter=delete_confirmation_getter,
)

archive_all_confirmation = Window(
    GetText("admin-category-archive-all-confirmation"),
    SwitchTo(
        GetText("inl-ui.archive"),
        id="archive",
        on_click=on_archive_all_categories,
        style=Style(ButtonStyle.DANGER),
        state=AdminCategoryState.categories,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminCategoryState.categories,
    ),
    state=AdminCategoryState.archive_all_confirmation,
)

delete_all_confirmation = Window(
    GetText("admin-category-delete-all-confirmation"),
    SwitchTo(
        GetText("inl-ui.delete"),
        id="delete",
        on_click=on_delete_all_categories,
        style=Style(ButtonStyle.DANGER),
        state=AdminCategoryState.categories,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=AdminCategoryState.categories,
    ),
    state=AdminCategoryState.delete_all_confirmation,
)
