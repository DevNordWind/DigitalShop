from aiogram import F
from aiogram.enums import ButtonStyle, ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Group, Select, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.style import Style
from domain.common.localized import Language
from presentation.aiogram.dialog.error import on_html_error
from presentation.aiogram.mapper.html import map_html
from presentation.aiogram.state import EditCategoryState
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import (
    on_delete_media,
    on_edit_description,
    on_edit_description_default_lang,
    on_edit_media,
    on_edit_name,
    on_edit_name_default_lang,
    on_remove_description,
    on_remove_name,
    on_select_description_lang,
    on_select_name_lang,
    on_translate_description_to_others,
    on_translate_name_to_others,
)
from .getter import (
    edit_description_default_lang_getter,
    edit_description_getter,
    edit_media_getter,
    edit_name_default_lang_getter,
    edit_name_getter,
)

edit_name = Window(
    GetText("admin-category-edit-name"),
    SwitchTo(
        GetText("admin-category-edit-name.default-lang-btn"),
        id="to_edit_default_lang",
        state=EditCategoryState.edit_name_default_lang,
        style=Style(ButtonStyle.PRIMARY),
    ),
    Group(
        Select(
            GetTextSelect("admin-category-edit-name.btn"),
            id="select_lang",
            items="buttons",
            item_id_getter=lambda item: item.lang,
            type_factory=Language,
            on_click=on_select_name_lang,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    TextInput(on_success=on_edit_name, id="input_new_name"),  # type: ignore[arg-type]
    Button(
        GetText("admin-category-edit-name.translate-btn"),
        id="translate",
        on_click=on_translate_name_to_others,
        when=F["can_translate_to_others"],
    ),
    Button(
        GetText("inl-ui.delete"),
        id="remove",
        on_click=on_remove_name,
        when=F["can_remove"],
    ),
    Cancel(GetText("inl-ui.back")),
    state=EditCategoryState.edit_name,
    getter=edit_name_getter,
)

edit_name_default_lang = Window(
    GetText("admin-category-edit-name-default-lang"),
    Group(
        Select(
            GetTextSelect("admin-category-edit-name-default-lang.btn"),
            id="select_lang",
            type_factory=Language,
            items="buttons",
            on_click=on_edit_name_default_lang,  # type: ignore[arg-type]
            item_id_getter=lambda item: item.lang,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=EditCategoryState.edit_name,
    ),
    state=EditCategoryState.edit_name_default_lang,
    getter=edit_name_default_lang_getter,
)

edit_description = Window(
    GetText("admin-category-edit-description"),
    SwitchTo(
        GetText("admin-category-edit-description.default-lang-btn"),
        id="to_default_lang",
        state=EditCategoryState.edit_description_default_lang,
        style=Style(ButtonStyle.PRIMARY),
        when=F["has_description"],
    ),
    Group(
        Select(
            GetTextSelect("admin-category-edit-description.btn"),
            id="select_lang",
            items="buttons",
            item_id_getter=lambda item: item.lang,
            type_factory=Language,
            on_click=on_select_description_lang,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    TextInput(
        on_success=on_edit_description,  # type: ignore[arg-type]
        id="input_new_name",
        type_factory=map_html,
        on_error=on_html_error,
    ),
    Button(
        GetText("admin-category-edit-description.translate-btn"),
        id="translate",
        on_click=on_translate_description_to_others,
        when=F["can_translate_to_others"],
    ),
    Button(
        GetText("inl-ui.delete"),
        id="remove",
        when=F["description"],
        on_click=on_remove_description,
    ),
    Cancel(GetText("inl-ui.back")),
    getter=edit_description_getter,
    state=EditCategoryState.edit_description,
)

edit_description_default_lang = Window(
    GetText("admin-category-edit-description-default-lang"),
    Group(
        Select(
            GetTextSelect("admin-category-edit-description-default-lang.btn"),
            id="select_lang",
            type_factory=Language,
            items="buttons",
            on_click=on_edit_description_default_lang,  # type: ignore[arg-type]
            item_id_getter=lambda item: item.lang,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=EditCategoryState.edit_name,
    ),
    state=EditCategoryState.edit_description_default_lang,
    getter=edit_description_default_lang_getter,
)

edit_media = Window(
    GetText("admin-category-edit-media"),
    DynamicMedia(selector="media", when=F["media"]),
    MessageInput(
        func=on_edit_media,
        content_types=[
            ContentType.ANIMATION,
            ContentType.PHOTO,
            ContentType.VIDEO,
        ],
    ),
    Button(
        GetText("inl-ui.delete"),
        id="delete_media",
        on_click=on_delete_media,
        when=F["media"],
    ),
    Cancel(GetText("inl-ui.back")),
    state=EditCategoryState.edit_media,
    getter=edit_media_getter,
)
