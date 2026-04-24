from aiogram_dialog import Dialog

from .callable import on_start, url_process_result
from .url_button import get_url_button_dialog
from .window import (
    broadcast,
    buttons,
    input_media,
    input_texts,
    preview,
    preview_select_lang,
)


def get_broadcast_dialogs() -> tuple[Dialog, Dialog]:
    return (
        Dialog(
            broadcast,
            preview,
            input_media,
            input_texts,
            buttons,
            preview_select_lang,
            on_start=on_start,
            on_process_result=url_process_result,
        ),
        get_url_button_dialog(),
    )
