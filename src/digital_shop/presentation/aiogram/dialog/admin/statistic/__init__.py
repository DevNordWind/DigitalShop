from aiogram_dialog import Dialog

from .callable import on_start
from .window import convert, input_period, statistic


def get_statistic_dialog() -> Dialog:
    return Dialog(statistic, convert, input_period, on_start=on_start)
