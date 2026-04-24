from aiogram_dialog import Dialog

from .callable import on_start
from .window import (
    input_description,
    input_media,
    input_name,
    input_price,
    select_warehouse,
    view,
)


def get_create_position_dialog() -> Dialog:
    return Dialog(
        view,
        input_media,
        input_description,
        input_name,
        input_price,
        select_warehouse,
        on_start=on_start,
    )
