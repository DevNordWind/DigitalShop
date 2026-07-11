from aiogram_dialog import Dialog

from .callable import on_start
from .window import input_commission, select_method, setting


def get_payment_settings_dialog() -> Dialog:
    return Dialog(select_method, setting, input_commission, on_start=on_start)
