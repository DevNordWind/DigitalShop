from aiogram_dialog import Dialog

from .callable import on_start
from .window import rates, related_rates


def get_rates_dialog() -> Dialog:
    return Dialog(rates, related_rates, on_start=on_start)
