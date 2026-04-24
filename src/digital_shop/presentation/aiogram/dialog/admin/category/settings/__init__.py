from aiogram_dialog import Dialog

from .window import default_lang, settings


def get_category_settings_dialog() -> Dialog:
    return Dialog(settings, default_lang)
