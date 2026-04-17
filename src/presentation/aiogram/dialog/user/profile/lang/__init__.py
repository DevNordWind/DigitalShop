from aiogram_dialog import Dialog

from .window import select_lang


def get_lang_dialog() -> Dialog:
    return Dialog(select_lang)
