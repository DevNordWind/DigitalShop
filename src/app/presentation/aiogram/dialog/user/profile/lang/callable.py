from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from dishka import AsyncContainer, FromDishka
from dishka.integrations.aiogram_dialog import inject

from aiogram import Bot
from aiogram.types import CallbackQuery
from app.domain.common.localized import Language
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.infra.authentication.telegram.handler import (
    UpdateTelegramLangCmd,
    UpdateTelegramLangHandler,
)
from app.presentation.aiogram.cmd import set_commands
from app.presentation.aiogram.port import Text


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

    bot: Bot = dialog_manager.middleware_data["bot"]
    ctx: TelegramContextDTO = await container.get(TelegramContextDTO)
    text: Text = await container.get(Text)
    await set_commands(bot=bot, text=text, user_role=ctx.user_role)
