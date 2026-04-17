from aiogram_dialog import Dialog

from .window import (
    general_settings,
    input_referral_percent,
    input_support_contact,
)


def get_general_settings_dialog() -> Dialog:
    return Dialog(
        general_settings, input_support_contact, input_referral_percent
    )
