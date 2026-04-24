from aiogram_dialog import Dialog

from .broadcast import get_broadcast_dialogs
from .callable import on_start
from .window import find, input_top_up_amount, user, users


def get_users_management_dialogs() -> tuple[Dialog, ...]:
    return Dialog(
        users, find, user, input_top_up_amount, on_start=on_start
    ), *get_broadcast_dialogs()
