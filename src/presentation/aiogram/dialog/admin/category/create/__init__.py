from aiogram_dialog import Dialog

from .callable import on_start
from .window import input_description, input_media, input_name, view


def get_create_category_dialog() -> Dialog:
    return Dialog(
        view,
        input_description,
        input_name,
        input_media,
        on_start=on_start,
    )
