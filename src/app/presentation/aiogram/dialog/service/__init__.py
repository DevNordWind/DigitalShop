from aiogram_dialog import Dialog

from .unselected_lang import get_unselected_lang_dialog


def get_service_dialogs() -> tuple[Dialog, ...]:
    return (get_unselected_lang_dialog(),)
