from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Group, Select, SwitchTo

from domain.common.money import Currency
from presentation.aiogram.state import CurrencyRatesState
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import on_select_source, on_select_target
from .getter import rates_getter, related_rates_getter

rates = Window(
    GetText("user-rates"),
    SwitchTo(
        GetText("user-rates.related-btn"),
        id="to_related",
        state=CurrencyRatesState.related_rates,
    ),
    Cancel(GetText("inl-ui.back")),
    state=CurrencyRatesState.rates,
    getter=rates_getter,
)

related_rates = Window(
    GetText("user-related-rates"),
    Button(GetText("user-related-rates.source-btn"), id="source"),
    Group(
        Select(
            GetTextSelect("user-related-rates.btn"),
            id="select_source_currency",
            type_factory=Currency,
            items="source_buttons",
            item_id_getter=lambda item: item.currency,
            on_click=on_select_source,  # type: ignore[arg-type]
        ),
        width=4,
    ),
    Button(GetText("user-related-rates.target-btn"), id="target"),
    Group(
        Select(
            GetTextSelect("user-related-rates.btn"),
            id="select_target_currency",
            type_factory=Currency,
            items="target_buttons",
            item_id_getter=lambda item: item.currency,
            on_click=on_select_target,  # type: ignore[arg-type]
        ),
        width=4,
    ),
    SwitchTo(
        GetText("inl-ui.back"), state=CurrencyRatesState.rates, id="back"
    ),
    getter=related_rates_getter,
    state=CurrencyRatesState.related_rates,
)
