from aiogram_dialog import Dialog

from .callable import on_start
from .window import (
    input_amount,
    input_code,
    input_percent,
    input_valid_from,
    input_valid_until,
    select_type,
    view,
)


def get_create_coupon_dialog() -> Dialog:
    return Dialog(
        view,
        input_percent,
        input_code,
        input_amount,
        input_valid_from,
        input_valid_until,
        select_type,
        on_start=on_start,
    )
