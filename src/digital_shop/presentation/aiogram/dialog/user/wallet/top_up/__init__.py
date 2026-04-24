from aiogram_dialog import Dialog

from .callable import on_start
from .window import (
    input_amount,
    payment,
    select_currency,
    select_payment_method,
)


def get_top_up_dialog() -> Dialog:
    return Dialog(
        payment,
        select_payment_method,
        select_currency,
        input_amount,
        on_start=on_start,
    )
