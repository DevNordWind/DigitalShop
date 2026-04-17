from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Group, Select, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia

from domain.common.localized import Language
from presentation.aiogram.dialog.error import on_html_error
from presentation.aiogram.mapper.html import map_html
from presentation.aiogram.state import CreateCategoryState
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import (
    on_clear_description,
    on_clear_media,
    on_confirm,
    on_input_description,
    on_input_media,
    on_input_name,
    on_select_description_lang,
    on_select_language,
    on_select_name_lang,
    on_translate_description_to_others,
    on_translate_name_to_others,
)
from .getter import (
    input_description_getter,
    input_media_getter,
    input_name_getter,
    view_getter,
)

view = Window(
    GetText("admin-category-create-view"),
    DynamicMedia(selector="media", when=F["media"]),
    Button(
        GetText("admin-category-create-view.show-language-btn"),
        id="show_language",
    ),
    Group(
        Select(
            GetTextSelect("admin-category-create-view.lang-btn"),
            items="buttons",
            item_id_getter=lambda item: item.lang,
            type_factory=Language,
            id="select_lang",
            on_click=on_select_language,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    Group(
        SwitchTo(
            GetText("admin-category-create-view.name-btn"),
            id="to_input_name",
            state=CreateCategoryState.input_name,
        ),
        SwitchTo(
            GetText("admin-category-create-view.description-btn"),
            id="to_input_description",
            state=CreateCategoryState.input_description,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("admin-category-create-view.media-btn"),
        id="to_input_media",
        state=CreateCategoryState.input_media,
    ),
    Button(
        GetText("inl-ui.confirm"),
        id="confirm",
        when=F["can_create"],
        on_click=on_confirm,
    ),
    Cancel(GetText("inl-ui.back")),
    state=CreateCategoryState.view,
    getter=view_getter,
)

input_name = Window(
    GetText("admin-category-create-name"),
    TextInput(on_success=on_input_name, type_factory=str, id="input_name"),  # type: ignore[arg-type]
    Group(
        Select(
            GetTextSelect("admin-category-create-name.btn"),
            id="select_lang",
            items="buttons",
            item_id_getter=lambda item: item.lang,
            type_factory=Language,
            on_click=on_select_name_lang,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    Button(
        GetText("admin-category-create-name.translate-btn"),
        on_click=on_translate_name_to_others,
        id="translate_name",
        when=F["can_translate_to_others"],
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=CreateCategoryState.view,
    ),
    getter=input_name_getter,
    state=CreateCategoryState.input_name,
)


input_description = Window(
    GetText("admin-category-create-description"),
    TextInput(
        on_success=on_input_description,  # type: ignore[arg-type]
        type_factory=map_html,
        on_error=on_html_error,
        id="input_description",
    ),
    Group(
        Select(
            GetTextSelect("admin-category-create-description.btn"),
            id="select_lang",
            items="buttons",
            item_id_getter=lambda item: item.lang,
            type_factory=Language,
            on_click=on_select_description_lang,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    Button(
        GetText("admin-category-create-description.translate-btn"),
        on_click=on_translate_description_to_others,
        id="translate_name",
        when=F["can_translate_to_others"],
    ),
    Button(
        GetText("inl-ui.clear"),
        on_click=on_clear_description,
        id="clear_description",
        when=F["description"],
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=CreateCategoryState.view,
    ),
    getter=input_description_getter,
    state=CreateCategoryState.input_description,
)

input_media = Window(
    GetText("admin-category-create-media"),
    MessageInput(
        func=on_input_media,
        content_types=(
            ContentType.PHOTO,
            ContentType.VIDEO,
            ContentType.ANIMATION,
        ),
    ),
    DynamicMedia(selector="media", when=F["media"]),
    Button(
        GetText("inl-ui.clear"),
        when=F["media"],
        on_click=on_clear_media,
        id="clear_media",
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=CreateCategoryState.view,
    ),
    getter=input_media_getter,
    state=CreateCategoryState.input_media,
)
