from aiogram_dialog import Dialog

from .info import get_info_dialog
from .profile import get_profile_dialogs
from .shopping import get_shopping_dialogs
from .wallet import get_wallet_dialogs


def get_user_dialogs() -> tuple[Dialog, ...]:
    return (
        *get_wallet_dialogs(),
        *get_shopping_dialogs(),
        *get_profile_dialogs(),
        get_info_dialog(),
    )
