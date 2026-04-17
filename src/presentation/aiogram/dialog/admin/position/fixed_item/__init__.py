from aiogram_dialog import Dialog

from .callable import on_start
from .window import (
    add,
    archive,
    archive_confirmation,
    archived_item,
    delete_confirmation,
    item,
    replace,
)


def get_fixed_item_dialog() -> Dialog:
    return Dialog(
        item,
        replace,
        add,
        archive_confirmation,
        delete_confirmation,
        archived_item,
        archive,
        on_start=on_start,
    )
