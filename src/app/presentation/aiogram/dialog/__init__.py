from aiogram_dialog import Dialog, LaunchMode

from .admin import get_admins_dialogs
from .service import get_service_dialogs
from .window import root


def get_root_dialog() -> Dialog:
    return Dialog(root, launch_mode=LaunchMode.ROOT)


__all__ = ("get_admins_dialogs", "get_root_dialog", "get_service_dialogs")
