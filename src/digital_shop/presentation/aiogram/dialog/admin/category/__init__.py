from aiogram_dialog import Dialog

from .callable import on_start
from .create import get_create_category_dialog
from .edit import get_edit_dialog
from .settings import get_category_settings_dialog
from .window import (
    archive_all_confirmation,
    archive_confirmation,
    categories,
    category,
    delete_all_confirmation,
    delete_confirmation,
    filters,
)


def get_categories_dialogs() -> tuple[Dialog, ...]:
    return (
        Dialog(
            categories,
            category,
            archive_confirmation,
            filters,
            delete_confirmation,
            delete_all_confirmation,
            archive_all_confirmation,
            on_start=on_start,
        ),
        get_create_category_dialog(),
        get_edit_dialog(),
        get_category_settings_dialog(),
    )
