from aiogram_dialog import Dialog

from .lang import get_lang_dialog
from .order import get_orders_dialog
from .referral import get_referral_dialogs
from .window import profile


def get_profile_dialogs() -> tuple[Dialog, ...]:
    return (
        Dialog(profile),
        get_orders_dialog(),
        get_lang_dialog(),
        *get_referral_dialogs(),
    )
