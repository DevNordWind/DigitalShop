from aiogram_dialog import Dialog

from .window import info


def get_info_dialog() -> Dialog:
    return Dialog(info)
