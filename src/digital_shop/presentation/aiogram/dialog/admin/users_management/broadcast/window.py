from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    ListGroup,
    Select,
    Start,
    SwitchTo,
    Url,
)
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format
from domain.common.localized import Language
from presentation.aiogram.dialog.admin.users_management.broadcast.callable import (  # noqa: E501
    on_delete_url_button,
    on_input_media,
    on_input_text,
    on_select_preview_lang,
    on_select_texts_lang,
    on_start_broadcast,
    on_switch_close_button,
)
from presentation.aiogram.dialog.admin.users_management.broadcast.getter import (  # noqa: E501
    broadcast_getter,
    buttons_getter,
    input_media_getter,
    input_texts_getter,
    preview_getter,
    preview_select_lang_getter,
)
from presentation.aiogram.dialog.error import on_html_error
from presentation.aiogram.mapper.html import map_html
from presentation.aiogram.state import BroadcastState, CreateUrlButtonState
from presentation.aiogram.widget import (
    GetText,
    GetTextSelect,
    InlineMarkupWidget,
)

broadcast = Window(
    GetText("admin-broadcast"),
    SwitchTo(
        GetText("admin-broadcast.preview-btn"),
        id="to_preview_select_lang",
        state=BroadcastState.preview_select_lang,
    ),
    Group(
        SwitchTo(
            GetText("admin-broadcast.buttons-btn"),
            id="to_buttons",
            state=BroadcastState.buttons,
        ),
        SwitchTo(
            GetText("admin-broadcast.texts-btn"),
            id="to_input_texts",
            state=BroadcastState.input_texts,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("admin-broadcast.media-btn"),
        id="to_input_media",
        state=BroadcastState.input_media,
    ),
    Button(
        GetText("admin-broadcast.start-btn"),
        id="start",
        when=F["can_start"],
        on_click=on_start_broadcast,
    ),
    Cancel(GetText("inl-ui.back"), id="back"),
    getter=broadcast_getter,
    state=BroadcastState.broadcast,
)

preview_select_lang = Window(
    GetText("admin-broadcast-preview-select-lang"),
    Button(
        GetText("admin-broadcast-preview-select-lang.show-language-btn"),
        id="show_language",
    ),
    Group(
        Select(
            GetTextSelect("admin-broadcast-preview-select-lang.lang-btn"),
            id="select_lang",
            type_factory=Language,
            items="buttons",
            on_click=on_select_preview_lang,  # type: ignore[arg-type]
            item_id_getter=lambda item: item.lang,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=BroadcastState.broadcast,
    ),
    state=BroadcastState.preview_select_lang,
    getter=preview_select_lang_getter,
)

preview = Window(
    GetText("admin-broadcast-preview"),
    DynamicMedia(selector="media", when=F["media"]),
    Button(GetText("inl-ui.close"), id="close", when=F["with_close_button"]),
    InlineMarkupWidget(selector="markup", id="markup", when=F["markup"]),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=BroadcastState.preview_select_lang,
    ),
    state=BroadcastState.preview,
    getter=preview_getter,
)

input_texts = Window(
    GetText("admin-broadcast-texts"),
    Group(
        Select(
            GetTextSelect("admin-broadcast-texts.btn"),
            id="select_lang",
            type_factory=Language,
            items="buttons",
            on_click=on_select_texts_lang,  # type: ignore[arg-type]
            item_id_getter=lambda item: item.lang,
        ),
        width=2,
    ),
    TextInput(
        on_success=on_input_text,
        id="input_text",
        type_factory=map_html,
        on_error=on_html_error,
    ),
    SwitchTo(
        GetText("inl-ui.back"), id="back", state=BroadcastState.broadcast
    ),
    state=BroadcastState.input_texts,
    getter=input_texts_getter,
)

input_media = Window(
    GetText("admin-broadcast-media"),
    DynamicMedia(selector="media", when=F["media"]),
    MessageInput(
        content_types=[
            ContentType.VIDEO,
            ContentType.ANIMATION,
            ContentType.PHOTO,
        ],
        id="input_media",
        func=on_input_media,
    ),
    SwitchTo(
        GetText("inl-ui.back"), id="back", state=BroadcastState.broadcast
    ),
    state=BroadcastState.input_media,
    getter=input_media_getter,
)

buttons = Window(
    GetText("admin-broadcast-buttons"),
    Group(
        ListGroup(
            Url(
                Format("{item.name}"),
                url=Format("{item.url}"),
                id="url_button",
            ),
            Button(Const("🗑"), id="delete", on_click=on_delete_url_button),
            item_id_getter=lambda item: item.index,
            id="url_buttons",
            items="buttons",
        ),
        width=2,
    ),
    Button(
        GetText("admin-broadcast-buttons.close-button-btn"),
        id="close_button_switcher",
        on_click=on_switch_close_button,
    ),
    Start(
        GetText("admin-broadcast-buttons.url-buttons-btn"),
        id="start_url",
        state=CreateUrlButtonState.url_button,
    ),
    SwitchTo(
        GetText("inl-ui.back"), id="back", state=BroadcastState.broadcast
    ),
    state=BroadcastState.buttons,
    getter=buttons_getter,
)
