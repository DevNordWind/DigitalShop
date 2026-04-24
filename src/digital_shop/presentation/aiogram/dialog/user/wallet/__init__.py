from aiogram_dialog import Dialog

from .callable import on_start
from .rates import get_rates_dialog
from .top_up import get_top_up_dialog
from .window import change_wallet, wallet


def get_wallet_dialogs() -> tuple[Dialog, ...]:
    return (
        Dialog(wallet, change_wallet, on_start=on_start),
        get_top_up_dialog(),
        get_rates_dialog(),
    )
