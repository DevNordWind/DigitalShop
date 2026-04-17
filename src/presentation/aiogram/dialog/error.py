from decimal import Decimal

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from presentation.aiogram.port import Text


@inject
async def on_decimal_error(
    event: Message,
    widget: ManagedTextInput[Decimal],
    dialog_manager: DialogManager,
    error: ValueError,
    text: FromDishka[Text],
) -> Message:
    return await event.reply(text=text("DecimalError"))


@inject
async def on_integer_error(
    event: Message,
    widget: ManagedTextInput[int],
    dialog_manager: DialogManager,
    error: ValueError,
    text: FromDishka[Text],
) -> Message:
    return await event.reply(text=text("IntegerError"))


@inject
async def on_html_error(
    event: Message,
    widget: ManagedTextInput[int],
    dialog_manager: DialogManager,
    error: ValueError,
    text: FromDishka[Text],
) -> Message:
    return await event.reply(text=text("HTMLValidationError"))
