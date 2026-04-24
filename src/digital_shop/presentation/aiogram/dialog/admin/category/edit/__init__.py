from aiogram_dialog import Dialog

from .callable import on_start
from .window import (
    edit_description,
    edit_description_default_lang,
    edit_media,
    edit_name,
    edit_name_default_lang,
)


def get_edit_dialog() -> Dialog:
    return Dialog(
        edit_name,
        edit_description,
        edit_media,
        edit_name_default_lang,
        edit_description_default_lang,
        on_start=on_start,
    )
