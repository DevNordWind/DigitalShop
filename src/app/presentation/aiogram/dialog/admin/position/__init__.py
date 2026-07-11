from aiogram_dialog import Dialog

from .callable import on_start
from .create import get_create_position_dialog
from .edit import get_position_edit_dialog
from .fixed_item import get_fixed_item_dialog
from .settings import get_position_settings_dialog
from .stock_item import get_stock_item_dialog
from .window import (
    archive_all_confirmation,
    archive_confirmation,
    category_filters,
    delete_all_confirmation,
    delete_confirmation,
    position,
    position_filters,
    select_category,
    select_position,
)


def get_position_dialogs() -> tuple[Dialog, ...]:
    return (
        Dialog(
            select_category,
            select_position,
            position,
            position_filters,
            category_filters,
            delete_confirmation,
            archive_confirmation,
            delete_all_confirmation,
            archive_all_confirmation,
            on_start=on_start,
        ),
        get_position_settings_dialog(),
        get_create_position_dialog(),
        get_position_edit_dialog(),
        get_fixed_item_dialog(),
        get_stock_item_dialog(),
    )
