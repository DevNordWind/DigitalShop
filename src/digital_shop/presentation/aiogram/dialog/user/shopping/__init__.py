from aiogram_dialog import Dialog

from .callable import on_start
from .order import get_order_dialog
from .window import (
    input_items_amount,
    position,
    select_category,
    select_position,
)


def get_shopping_dialogs() -> tuple[Dialog, ...]:
    return Dialog(
        select_category,
        select_position,
        position,
        input_items_amount,
        on_start=on_start,
    ), get_order_dialog()
