from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    Select,
    SwitchTo,
    Url,
)
from aiogram_dialog.widgets.text import Format

from presentation.aiogram.state import CreateUrlButtonState
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import (
    on_create,
    on_input_name,
    on_input_url,
    on_input_url_error,
    on_select_lang,
    on_select_name_lang,
    validate_url,
)
from .getter import input_name_getter, input_url_getter, url_button_getter

url_button = Window(
    GetText("admin-broadcast-buttons-url-create"),
    Url(
        text=Format("{button_name}"),
        url=Format("{button_url}"),
        when=(F["button_url"]) & (F["button_name"]),
    ),
    Button(
        GetText("admin-broadcast-buttons-url-create.show-language-btn"),
        id="show_language",
    ),
    Group(
        Select(
            GetTextSelect("admin-broadcast-buttons-url-create.lang-btn"),
            items="buttons",
            item_id_getter=lambda item: item.lang,
            on_click=on_select_lang,  # type: ignore[arg-type]
            id="select_lang",
        ),
        width=2,
    ),
    SwitchTo(
        GetText("admin-broadcast-buttons-url-create.names-btn"),
        id="to_input_name",
        state=CreateUrlButtonState.input_name,
    ),
    SwitchTo(
        GetText("admin-broadcast-buttons-url-create.url-btn"),
        id="to_input_url",
        state=CreateUrlButtonState.input_url,
    ),
    Button(
        GetText("inl-ui.create"),
        id="create",
        when=F["can_create"],
        on_click=on_create,
    ),
    Cancel(GetText("inl-ui.back")),
    state=CreateUrlButtonState.url_button,
    getter=url_button_getter,
)

input_name = Window(
    GetText("admin-broadcast-buttons-url-text"),
    TextInput(on_success=on_input_name, id="input_name"),
    Group(
        Select(
            GetTextSelect("admin-broadcast-buttons-url-text.btn"),
            items="buttons",
            item_id_getter=lambda item: item.lang,
            on_click=on_select_name_lang,  # type: ignore[arg-type]
            id="select_lang",
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=CreateUrlButtonState.url_button,
    ),
    getter=input_name_getter,
    state=CreateUrlButtonState.input_name,
)

input_url = Window(
    GetText("admin-broadcast-buttons-url-url"),
    TextInput(
        on_success=on_input_url,
        id="input_url",
        on_error=on_input_url_error,
        type_factory=validate_url,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=CreateUrlButtonState.url_button,
    ),
    getter=input_url_getter,
    state=CreateUrlButtonState.input_url,
)
