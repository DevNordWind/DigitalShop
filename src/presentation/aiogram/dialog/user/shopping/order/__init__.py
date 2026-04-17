from aiogram_dialog import Dialog

from .callable import on_start
from .window import (
    input_coupon_code,
    input_new_items_amount,
    order,
    payment,
    select_payment_method,
)


def get_order_dialog() -> Dialog:
    return Dialog(
        order,
        payment,
        input_new_items_amount,
        input_coupon_code,
        select_payment_method,
        on_start=on_start,
    )
