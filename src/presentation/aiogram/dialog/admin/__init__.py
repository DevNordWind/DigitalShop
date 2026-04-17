from aiogram_dialog import Dialog

from .category import get_categories_dialogs
from .coupon import get_coupon_dialogs
from .general_settings import get_general_settings_dialog
from .payment_settings import get_payment_settings_dialog
from .position import get_position_dialogs
from .statistic import get_statistic_dialog
from .users_management import get_users_management_dialogs
from .window import root


def get_admins_dialogs() -> tuple[Dialog, ...]:
    root_admin_dialog = Dialog(root)

    return (
        root_admin_dialog,
        *get_categories_dialogs(),
        get_payment_settings_dialog(),
        *get_position_dialogs(),
        *get_coupon_dialogs(),
        *get_users_management_dialogs(),
        get_general_settings_dialog(),
        get_statistic_dialog(),
    )
