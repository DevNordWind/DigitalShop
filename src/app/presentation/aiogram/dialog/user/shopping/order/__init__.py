from aiogram_dialog import Dialog

from .callable import on_start
from .window import (
    input_coupon_code,
    order,
    payment,
    payment_confirmed,
    select_payment_method,
)


def get_order_dialog() -> Dialog:
    return Dialog(
        order,
        payment,
        input_coupon_code,
        select_payment_method,
        payment_confirmed,
        on_start=on_start,  # type: ignore[bad-argument-type]
    )
