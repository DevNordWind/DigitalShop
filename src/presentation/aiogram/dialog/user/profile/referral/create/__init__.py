from aiogram_dialog import Dialog

from .window import select_currency


def get_create_referrer_profile_dialog() -> Dialog:
    return Dialog(select_currency)
