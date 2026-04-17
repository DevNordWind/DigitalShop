from aiogram import F
from aiogram.enums import ContentType
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

from domain.common.localized import Language
from domain.common.money import Currency
from domain.product.position.enums.warehouse import WarehouseType
from presentation.aiogram.dialog.error import on_decimal_error, on_html_error
from presentation.aiogram.mapper.decimal import map_decimal
from presentation.aiogram.mapper.html import map_html
from presentation.aiogram.state import CreatePositionState
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import (
    on_clear_description,
    on_clear_name,
    on_confirm,
    on_convert_price_to_others,
    on_input_description,
    on_input_media,
    on_input_name,
    on_input_price,
    on_remove_media,
    on_select_currency,
    on_select_description_lang,
    on_select_language,
    on_select_name_lang,
    on_select_warehouse,
    on_translate_description_to_others,
    on_translate_name_to_others,
)
from .ctx import MEDIA_SCROLL
from .getter import (
    input_description_getter,
    input_media_getter,
    input_name_getter,
    input_price_getter,
    select_warehouse_getter,
    view_getter,
)

view = Window(
    GetText("admin-position-create-view"),
    Button(
        GetText("admin-position-create-view.show-language-btn"),
        id="show_language",
    ),
    Group(
        Select(
            GetTextSelect("admin-position-create-view.lang-btn"),
            id="select_language",
            type_factory=Language,
            items="buttons",
            item_id_getter=lambda item: item.lang,
            on_click=on_select_language,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    SwitchTo(
        GetText("admin-position-create-view.name-btn"),
        id="to_name",
        state=CreatePositionState.input_name,
    ),
    SwitchTo(
        GetText("admin-position-create-view.description-btn"),
        id="to_description",
        state=CreatePositionState.input_description,
    ),
    SwitchTo(
        GetText("admin-position-create-view.price-btn"),
        id="to_price",
        state=CreatePositionState.input_price,
    ),
    Group(
        SwitchTo(
            GetText("admin-position-create-view.media-btn"),
            id="to_media",
            state=CreatePositionState.input_media,
        ),
        SwitchTo(
            GetText("admin-position-create-view.items-btn"),
            id="to_items",
            state=CreatePositionState.select_warehouse,
        ),
        width=2,
    ),
    Button(
        GetText("inl-ui.confirm"),
        id="confirm",
        on_click=on_confirm,
        when=F["can_confirm"],
    ),
    Cancel(
        GetText("inl-ui.back"),
    ),
    state=CreatePositionState.view,
    getter=view_getter,
)

input_name = Window(
    GetText("admin-position-create-name"),
    TextInput(on_success=on_input_name, id="input_name"),  # type: ignore[arg-type]
    Group(
        Select(
            GetTextSelect("admin-position-create-name.btn"),
            id="select_lang",
            on_click=on_select_name_lang,  # type: ignore[arg-type]
            items="buttons",
            type_factory=Language,
            item_id_getter=lambda item: item.lang,
        ),
        width=2,
    ),
    Button(
        GetText("admin-position-create-name.translate-btn"),
        id="translate",
        on_click=on_translate_name_to_others,
        when=F["can_translate_to_others"],
    ),
    Button(
        GetText("inl-ui.clear"),
        id="clear",
        on_click=on_clear_name,
        when=F["can_clear"],
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=CreatePositionState.view,
    ),
    state=CreatePositionState.input_name,
    getter=input_name_getter,
)

input_description = Window(
    GetText("admin-position-create-description"),
    TextInput(
        on_success=on_input_description,
        on_error=on_html_error,
        type_factory=map_html,
        id="input_description",
    ),
    Group(
        Select(
            GetTextSelect("admin-position-create-description.btn"),
            id="select_lang",
            on_click=on_select_description_lang,  # type: ignore[arg-type]
            items="buttons",
            type_factory=Language,
            item_id_getter=lambda item: item.lang,
        ),
        width=2,
    ),
    Button(
        GetText("admin-position-create-description.translate-btn"),
        id="translate",
        on_click=on_translate_description_to_others,
        when=F["can_translate_to_others"],
    ),
    Button(
        GetText("inl-ui.clear"),
        id="clear",
        on_click=on_clear_description,
        when=F["description"],
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=CreatePositionState.view,
    ),
    state=CreatePositionState.input_description,
    getter=input_description_getter,
)

input_price = Window(
    GetText("admin-position-create-price"),
    TextInput(
        on_success=on_input_price,
        id="input_price",
        on_error=on_decimal_error,
        type_factory=map_decimal,
    ),
    Group(
        Select(
            GetTextSelect("admin-position-create-price.btn"),
            id="select_currency",
            on_click=on_select_currency,  # type: ignore[arg-type]
            items="buttons",
            type_factory=Currency,
            item_id_getter=lambda item: item.currency,
        ),
        width=2,
    ),
    Button(
        GetText("admin-position-create-price.convert-btn"),
        id="convert",
        on_click=on_convert_price_to_others,
        when=F["can_convert_to_others"],
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=CreatePositionState.view,
    ),
    state=CreatePositionState.input_price,
    getter=input_price_getter,
)

input_media = Window(
    GetText("admin-position-create-media"),
    DynamicMedia(selector="media", when=F["media"]),
    MessageInput(
        func=on_input_media,
        content_types=(
            ContentType.PHOTO,
            ContentType.VIDEO,
            ContentType.ANIMATION,
        ),
        id="input_media",
    ),
    StubScroll(id=MEDIA_SCROLL, pages="pages"),
    NumberedPager(scroll=MEDIA_SCROLL, when=F["pages"] > 0),
    Button(
        GetText("inl-ui.delete"),
        on_click=on_remove_media,
        when=F["pages"] > 0,
        id="remove_media",
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        state=CreatePositionState.view,
        id="back",
    ),
    getter=input_media_getter,
    state=CreatePositionState.input_media,
)

select_warehouse = Window(
    GetText("admin-position-create-warehouse"),
    Group(
        Select(
            GetTextSelect("admin-position-create-warehouse.btn"),
            id="select_warehouse",
            items="buttons",
            item_id_getter=lambda item: item.type,
            type_factory=WarehouseType,
            on_click=on_select_warehouse,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        state=CreatePositionState.view,
        id="back",
    ),
    getter=select_warehouse_getter,
    state=CreatePositionState.select_warehouse,
)
