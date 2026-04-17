from uuid import UUID

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
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

from presentation.aiogram.dialog.error import on_integer_error
from presentation.aiogram.state import ShoppingState
from presentation.aiogram.widget import GetText, GetTextSelect, Pagination

from .callable import (
    on_buy,
    on_input_items_amount,
    on_select_category,
    on_select_position,
)
from .ctx import CATEGORIES_SCROLL, POSITION_MEDIA_SCROLL, POSITIONS_SCROLL
from .getter import (
    input_items_amount_getter,
    position_getter,
    select_category_getter,
    select_position_getter,
)

select_category = Window(
    GetText("user-shopping-category"),
    Group(
        Select(
            GetTextSelect("user-shopping-category.btn"),
            id="s_c",
            items="buttons",
            item_id_getter=lambda item: item.id,
            type_factory=UUID,
            on_click=on_select_category,  # type: ignore[arg-type]
        ),
        width=1,
    ),
    Pagination(scroll_id=CATEGORIES_SCROLL),
    Cancel(GetText("inl-ui.back")),
    state=ShoppingState.select_category,
    getter=select_category_getter,
)

select_position = Window(
    GetText("user-shopping-position"),
    DynamicMedia(selector="media", when=F["media"]),
    Group(
        Select(
            GetTextSelect("user-shopping-position.btn"),
            id="s_p",
            items="buttons",
            item_id_getter=lambda item: item.id,
            type_factory=UUID,
            on_click=on_select_position,  # type: ignore[arg-type]
        ),
        width=1,
    ),
    Pagination(scroll_id=POSITIONS_SCROLL),
    SwitchTo(
        GetText("inl-ui.back"),
        state=ShoppingState.select_category,
        id="back",
    ),
    state=ShoppingState.select_position,
    getter=select_position_getter,
)

position = Window(
    GetText("user-position"),
    DynamicMedia(selector="media", when=F["media"]),
    StubScroll(id=POSITION_MEDIA_SCROLL, pages="pages"),
    NumberedPager(scroll=POSITION_MEDIA_SCROLL, when=F["pages"] > 1),
    Button(
        GetText(
            "user-position.buy-btn",
        ),
        id="buy",
        on_click=on_buy,
        when=F["items_amount"] > 0,
    ),
    SwitchTo(
        GetText("inl-ui.back"),
        id="back",
        state=ShoppingState.select_position,
    ),
    state=ShoppingState.position,
    getter=position_getter,
)

input_items_amount = Window(
    GetText("user-position-items-amount-stock"),
    TextInput(
        on_success=on_input_items_amount,
        on_error=on_integer_error,
        type_factory=int,
        id="input_items_amount",
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=ShoppingState.position),
    state=ShoppingState.input_items_amount,
    getter=input_items_amount_getter,
)
