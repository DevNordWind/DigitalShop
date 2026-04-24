from decimal import Decimal

from aiogram import F
from aiogram.enums import ButtonStyle, ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    NumberedPager,
    Select,
    StubScroll,
    SwitchTo,
)
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.style import Style
from domain.common.localized import Language
from domain.common.money import Currency
from presentation.aiogram.dialog.admin.position.edit.callable import (
    on_change_description_default_lang,
    on_change_name_default_lang,
    on_change_price_base_currency,
    on_convert_price_to_others,
    on_edit_description,
    on_edit_media,
    on_edit_name,
    on_edit_price,
    on_remove_description,
    on_remove_media,
    on_remove_name,
    on_select_currency,
    on_select_description_lang,
    on_select_mode,
    on_select_name_lang,
    on_translate_description_to_others,
    on_translate_name_to_others,
)
from presentation.aiogram.dialog.admin.position.edit.ctx import (
    EDIT_POSITION_MEDIA_SCROLL,
    MediaEditingMode,
)
from presentation.aiogram.dialog.admin.position.edit.getter import (
    edit_description_default_lang,
    edit_description_getter,
    edit_media_getter,
    edit_name_default_lang,
    edit_name_getter,
    edit_price_base_currency_getter,
    edit_price_getter,
)
from presentation.aiogram.dialog.error import on_decimal_error, on_html_error
from presentation.aiogram.mapper.decimal import map_decimal
from presentation.aiogram.mapper.html import map_html
from presentation.aiogram.state import EditPositionState
from presentation.aiogram.widget import GetText, GetTextSelect

edit_name = Window(
    GetText("admin-position-edit-name"),
    TextInput(on_success=on_edit_name, id="input_name"),
    SwitchTo(
        GetText("admin-position-edit-name.default-lang-btn"),
        state=EditPositionState.edit_name_default_lang,
        id="to_default_lang",
        style=Style(ButtonStyle.PRIMARY),
    ),
    Group(
        Select(
            GetTextSelect("admin-position-edit-name.btn"),
            id="select_lang",
            type_factory=Language,
            items="buttons",
            item_id_getter=lambda item: item.lang,
            on_click=on_select_name_lang,  # type: ignore[arg-type]
        ),
    ),
    Button(
        GetText("admin-position-edit-name.translate-btn"),
        id="translate",
        when=F["can_translate_to_others"],
        on_click=on_translate_name_to_others,
    ),
    Button(
        GetText("inl-ui.delete"),
        id="remove",
        on_click=on_remove_name,
        when=F["can_remove"],
    ),
    Cancel(GetText("inl-ui.back")),
    getter=edit_name_getter,
    state=EditPositionState.edit_name,
)

change_name_default_lang = Window(
    GetText("admin-position-edit-name-default-lang"),
    Group(
        Select(
            GetTextSelect("admin-position-edit-name-default-lang.btn"),
            id="select_lang",
            on_click=on_change_name_default_lang,  # type: ignore[arg-type]
            items="buttons",
            item_id_getter=lambda item: item.lang,
            type_factory=Language,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=EditPositionState.edit_name,
    ),
    state=EditPositionState.edit_name_default_lang,
    getter=edit_name_default_lang,
)

edit_description = Window(
    GetText("admin-position-edit-description"),
    TextInput(
        on_success=on_edit_description,
        id="input_description",
        on_error=on_html_error,
        type_factory=map_html,
    ),
    SwitchTo(
        GetText("admin-position-edit-description.default-lang-btn"),
        state=EditPositionState.edit_description_default_lang,
        id="to_default_lang",
        style=Style(ButtonStyle.PRIMARY),
        when=F["can_change_default_lang"],
    ),
    Group(
        Select(
            GetTextSelect("admin-position-edit-description.btn"),
            id="select_lang",
            type_factory=Language,
            items="buttons",
            item_id_getter=lambda item: item.lang,
            on_click=on_select_description_lang,  # type: ignore[arg-type]
        ),
    ),
    Button(
        GetText("admin-position-edit-description.translate-btn"),
        id="translate",
        when=F["can_translate_to_others"],
        on_click=on_translate_description_to_others,
    ),
    Button(
        GetText("inl-ui.delete"),
        id="remove",
        on_click=on_remove_description,
        when=F["description"],
    ),
    Cancel(GetText("inl-ui.back")),
    getter=edit_description_getter,
    state=EditPositionState.edit_description,
)

change_description_default_lang = Window(
    GetText("admin-position-edit-description-default-lang"),
    Group(
        Select(
            GetTextSelect("admin-position-edit-description-default-lang.btn"),
            id="select_lang",
            on_click=on_change_description_default_lang,  # type: ignore[arg-type]
            items="buttons",
            item_id_getter=lambda item: item.lang,
            type_factory=Language,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=EditPositionState.edit_description,
    ),
    state=EditPositionState.edit_description_default_lang,
    getter=edit_description_default_lang,
)

edit_price = Window(
    GetText("admin-position-edit-price"),
    SwitchTo(
        GetText("admin-position-edit-price.base-currency-btn"),
        id="to_base_currency",
        state=EditPositionState.edit_price_base_currency,
        style=Style(ButtonStyle.PRIMARY),
    ),
    TextInput[Decimal](
        on_success=on_edit_price,  # type: ignore[arg-type]
        type_factory=map_decimal,
        on_error=on_decimal_error,
        id="input_price",
    ),
    Group(
        Select(
            GetTextSelect("admin-position-edit-price.btn"),
            id="select_currency",
            item_id_getter=lambda item: item.currency,
            type_factory=Currency,
            on_click=on_select_currency,  # type: ignore[arg-type]
            items="buttons",
        ),
        width=2,
    ),
    Button(
        GetText("admin-position-edit-price.convert-btn"),
        id="convert_currency",
        on_click=on_convert_price_to_others,
        when=F["can_convert_to_others"],
    ),
    Cancel(
        GetText("inl-ui.back"),
    ),
    getter=edit_price_getter,
    state=EditPositionState.edit_price,
)

change_price_base_currency = Window(
    GetText("admin-position-edit-base-currency"),
    Group(
        Select(
            GetTextSelect("admin-position-edit-base-currency.btn"),
            id="select_currency",
            on_click=on_change_price_base_currency,  # type: ignore[arg-type]
            items="buttons",
            item_id_getter=lambda item: item.currency,
            type_factory=Currency,
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=EditPositionState.edit_price,
    ),
    state=EditPositionState.edit_price_base_currency,
    getter=edit_price_base_currency_getter,
)

edit_media = Window(
    GetText("admin-position-edit-media"),
    DynamicMedia(selector="media", when=F["media"]),
    StubScroll(id=EDIT_POSITION_MEDIA_SCROLL, pages="pages"),
    NumberedPager(scroll=EDIT_POSITION_MEDIA_SCROLL, when=F["pages"] > 1),
    MessageInput(
        content_types=(
            ContentType.PHOTO,
            ContentType.VIDEO,
            ContentType.ANIMATION,
        ),
        func=on_edit_media,
        id="input_media",
    ),
    Button(GetText("admin-position-edit-media.mode-btn"), id="mode"),
    Group(
        Select(
            GetTextSelect("admin-position-edit-media.btn"),
            id="select_mode",
            type_factory=MediaEditingMode,
            item_id_getter=lambda item: item.mode,
            items="buttons",
            on_click=on_select_mode,
        ),
        width=2,
    ),
    Button(
        GetText("inl-ui.delete"),
        id="delete",
        on_click=on_remove_media,
        when=F["media"],
    ),
    Cancel(
        GetText("inl-ui.back"),
    ),
    state=EditPositionState.edit_media,
    getter=edit_media_getter,
)
