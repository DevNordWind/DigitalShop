from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from dishka import AsyncContainer, FromDishka
from dishka.integrations.aiogram_dialog import inject

from domain.common.localized import Language
from infra.authentication.telegram.handler import (
    UpdateTelegramLangCmd,
    UpdateTelegramLangHandler,
)


@inject
async def on_select_lang(
    event: CallbackQuery,
    widget: Select[Language],
    dialog_manager: DialogManager,
    lang: Language,
    handler: FromDishka[UpdateTelegramLangHandler],
    container: FromDishka[AsyncContainer],
) -> None:
    await handler.execute(data=UpdateTelegramLangCmd(new_lang=lang))
    await container.close()
