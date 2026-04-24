from aiogram_dialog import Dialog

from .window import default_currency, default_lang, settings


def get_position_settings_dialog() -> Dialog:
    return Dialog(settings, default_lang, default_currency)
