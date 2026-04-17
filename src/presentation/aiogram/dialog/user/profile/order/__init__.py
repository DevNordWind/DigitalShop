from aiogram_dialog import Dialog

from .callable import on_start
from .window import filters, order, orders


def get_orders_dialog() -> Dialog:
    return Dialog(order, orders, filters, on_start=on_start)
