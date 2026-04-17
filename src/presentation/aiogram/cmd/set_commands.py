from aiogram import Bot
from aiogram.types import BotCommand

from domain.user.enums import UserRole
from presentation.aiogram.port import Text

COMMANDS: tuple[str, ...] = (
    "start",
    "buy",
    "wallet",
    "profile",
    "info",
)


async def set_commands(bot: Bot, user_role: UserRole, text: Text) -> bool:
    commands: list[BotCommand] = [
        BotCommand(command=cmd, description=text(f"bot-commands.{cmd}"))
        for cmd in COMMANDS
    ]
    if user_role >= UserRole.ADMIN:
        commands.append(
            BotCommand(command="admin", description=text("bot-commands.admin"))
        )
    return await bot.set_my_commands(commands=commands)
