from aiogram_dialog import Dialog, LaunchMode

from .window import select_lang


def get_unselected_lang_dialog() -> Dialog:
    return Dialog(select_lang, launch_mode=LaunchMode.ROOT)
