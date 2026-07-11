from contextlib import suppress

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import AsyncContainer, FromDishka
from dishka.integrations.aiogram_dialog import inject

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import CallbackQuery, Message
from app.domain.common.localized import Language
from app.domain.user.enums import UserRole
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.infra.authentication.telegram.handler import (
    SetTelegramLangCmd,
    SetTelegramLangHandler,
)
from app.presentation.aiogram.cmd import set_commands
from app.presentation.aiogram.kb import ServiceKeyboard
from app.presentation.aiogram.port import Text
from app.presentation.aiogram.setting.general import GeneralBotSettings
from app.presentation.aiogram.state import RootState


@inject
async def on_select_lang(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    lang: Language,
    handler: FromDishka[SetTelegramLangHandler],
    settings: FromDishka[GeneralBotSettings],
    container: FromDishka[AsyncContainer],
    kb: FromDishka[ServiceKeyboard],
) -> None:
    await handler.execute(SetTelegramLangCmd(lang=lang))
    await container.close()

    bot: Bot = dialog_manager.middleware_data["bot"]
    ctx: TelegramContextDTO = await container.get(TelegramContextDTO)
    text: Text = await container.get(Text)
    await set_commands(bot=bot, text=text, user_role=ctx.user_role)

    if settings.tech_work.status and ctx.user_role < UserRole.ADMIN:
        with suppress(TelegramAPIError):
            if isinstance(event.message, Message):
                await event.message.delete()

        await dialog_manager.done()

        return await event.message.answer(  # type: ignore[union-attr]
            text=text("tech-work"),
            reply_markup=kb.get_tech_work_markup(
                support_url=getattr(settings.support, "url", None)
            ),
        )

    return await dialog_manager.start(state=RootState.root)
