from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    Select,
    Start,
    SwitchTo,
)
from domain.common.money import Currency
from presentation.aiogram.state import (
    CurrencyRatesState,
    TopUpState,
    WalletState,
)
from presentation.aiogram.widget import GetText, GetTextSelect

from .callable import on_change_wallet, on_switch_show_all_balances
from .getter import change_wallet_getter, wallet_getter

wallet = Window(
    GetText("wallet"),
    Button(
        GetText("wallet.show-all-btn"),
        id="show_all",
        on_click=on_switch_show_all_balances,
    ),
    Group(
        Start(
            GetText("wallet.top-up-btn"),
            id="top_up",
            state=TopUpState.input_amount,
        ),
        SwitchTo(
            GetText("wallet.change-wallet-btn"),
            id="tp_change_wallet",
            state=WalletState.change_wallet,
        ),
        width=2,
    ),
    Start(
        GetText("wallet.rates-btn"),
        id="to_rates",
        state=CurrencyRatesState.rates,
    ),
    Cancel(GetText("inl-ui.back")),
    state=WalletState.wallet,
    getter=wallet_getter,
)

change_wallet = Window(
    GetText("wallet-change-wallet"),
    Group(
        Select(
            GetTextSelect("wallet-change-wallet.btn"),
            id="select_currency",
            on_click=on_change_wallet,  # type: ignore[arg-type]
            type_factory=Currency,
            items="buttons",
            item_id_getter=lambda item: item.currency,
        ),
        width=2,
    ),
    SwitchTo(GetText("inl-ui.back"), id="back", state=WalletState.wallet),
    getter=change_wallet_getter,
    state=WalletState.change_wallet,
)
