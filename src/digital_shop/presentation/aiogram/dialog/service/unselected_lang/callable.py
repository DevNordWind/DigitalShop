from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import AsyncContainer, FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.localized import Language
from infra.authentication.telegram.dto import TelegramContextDTO
from infra.authentication.telegram.handler import (
    UpdateTelegramLangCmd,
    UpdateTelegramLangHandler,
)
from presentation.aiogram.cmd import set_commands
from presentation.aiogram.port import Text
from presentation.aiogram.state import RootState


@inject
async def on_select_lang(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    new_lang: Language,
    handler: FromDishka[UpdateTelegramLangHandler],
    container: FromDishka[AsyncContainer],
) -> None:
    await handler.execute(UpdateTelegramLangCmd(new_lang=new_lang))
    await container.close()

    bot: Bot = dialog_manager.middleware_data["bot"]
    ctx: TelegramContextDTO = await container.get(TelegramContextDTO)
    text: Text = await container.get(Text)
    await set_commands(bot=bot, text=text, user_role=ctx.user_role)

    return await dialog_manager.start(state=RootState.root)
