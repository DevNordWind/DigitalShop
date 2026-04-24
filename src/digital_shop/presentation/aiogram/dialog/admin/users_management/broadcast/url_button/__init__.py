from aiogram_dialog import Dialog

from .callable import on_start
from .window import input_name, input_url, url_button


def get_url_button_dialog() -> Dialog:
    return Dialog(url_button, input_name, input_url, on_start=on_start)
