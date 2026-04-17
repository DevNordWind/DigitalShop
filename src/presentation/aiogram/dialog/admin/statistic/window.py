from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Group, Select, SwitchTo

from domain.common.money import Currency
from presentation.aiogram.state import AdminStatisticState
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import (
    map_period,
    map_period_unit,
    on_input_period,
    on_input_period_error,
    on_select_currency,
    on_select_period,
)
from .getter import convert_getter, input_period_getter, statistic_getter

statistic = Window(
    GetText("admin-statistic"),
    Group(
        Select(
            GetTextSelect("admin-statistic.period-unit-btn"),
            items="buttons",
            item_id_getter=lambda item: item.unit,
            type_factory=map_period_unit,
            on_click=on_select_period,  # type: ignore[arg-type]
            id="select_period",
        ),
        width=2,
    ),
    SwitchTo(
        GetText("admin-statistic.period-btn"),
        id="to_input_period",
        state=AdminStatisticState.input_period,
    ),
    SwitchTo(
        GetText("admin-statistic.convert-btn"),
        id="to_convert",
        state=AdminStatisticState.convert,
    ),
    Cancel(GetText("inl-ui.back")),
    state=AdminStatisticState.statistic,
    getter=statistic_getter,
)

input_period = Window(
    GetText("admin-statistic-period"),
    TextInput(
        on_success=on_input_period,
        on_error=on_input_period_error,
        type_factory=map_period,
        id="input_period",
    ),
    SwitchTo(
        GetText("inl-ui.back"), id="back", state=AdminStatisticState.statistic
    ),
    getter=input_period_getter,
    state=AdminStatisticState.input_period,
)

convert = Window(
    GetText("admin-statistic-convert"),
    Group(
        Select(
            GetTextSelect("admin-statistic-convert.btn"),
            id="select_currency",
            type_factory=Currency,
            items="buttons",
            item_id_getter=lambda item: item.currency,
            on_click=on_select_currency,  # type: ignore[arg-type]
        ),
        width=2,
    ),
    SwitchTo(
        GetText("inl-ui.back"), id="back", state=AdminStatisticState.statistic
    ),
    getter=convert_getter,
    state=AdminStatisticState.convert,
)
