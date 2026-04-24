from aiogram_dialog import Dialog

from .callable import on_start
from .create import get_create_coupon_dialog
from .window import coupon, coupons, filters


def get_coupon_dialogs() -> tuple[Dialog, ...]:
    return (
        Dialog(coupons, coupon, filters, on_start=on_start),
        get_create_coupon_dialog(),
    )
