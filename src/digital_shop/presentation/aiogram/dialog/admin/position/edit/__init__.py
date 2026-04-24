from aiogram_dialog import Dialog

from .callable import on_start
from .window import (
    change_description_default_lang,
    change_name_default_lang,
    change_price_base_currency,
    edit_description,
    edit_media,
    edit_name,
    edit_price,
)


def get_position_edit_dialog() -> Dialog:
    return Dialog(
        change_price_base_currency,
        change_description_default_lang,
        change_name_default_lang,
        edit_description,
        edit_media,
        edit_name,
        edit_price,
        on_start=on_start,
    )
