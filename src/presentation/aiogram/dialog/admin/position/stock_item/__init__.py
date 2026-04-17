from aiogram_dialog import Dialog

from .callable import on_start
from .window import (
    add,
    archive_all_confirmation,
    archive_confirmation,
    delete_all_confirmation,
    delete_confirmation,
    filters,
    item,
    items,
)


def get_stock_item_dialog() -> Dialog:
    return Dialog(
        item,
        items,
        add,
        filters,
        archive_confirmation,
        archive_all_confirmation,
        delete_confirmation,
        delete_all_confirmation,
        on_start=on_start,
    )
