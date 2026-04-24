from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager
from presentation.aiogram.filter import IsAdmin
from presentation.aiogram.state import (
    AdminRootState,
    InfoState,
    ProfileState,
    RootState,
    ShoppingState,
    WalletState,
)


def get_command_router() -> Router:
    command_router = Router()
    command_router.message.register(on_start, CommandStart())
    command_router.message.register(on_profile, Command("profile"))
    command_router.message.register(on_info, Command("info"))
    command_router.message.register(on_buy, Command("buy"))
    command_router.message.register(on_wallet, Command("wallet"))
    command_router.message.register(
        on_admin_panel, Command("admin"), IsAdmin()
    )

    return command_router


async def on_start(_: Message, dialog_manager: DialogManager) -> None:
    return await dialog_manager.start(state=RootState.root)


async def on_profile(_: Message, dialog_manager: DialogManager) -> None:
    return await dialog_manager.start(state=ProfileState.profile)


async def on_info(_: Message, dialog_manager: DialogManager) -> None:
    return await dialog_manager.start(state=InfoState.info)


async def on_buy(_: Message, dialog_manager: DialogManager) -> None:
    return await dialog_manager.start(state=ShoppingState.select_category)


async def on_wallet(_: Message, dialog_manager: DialogManager) -> None:
    return await dialog_manager.start(state=WalletState.wallet)


async def on_admin_panel(_: Message, dialog_manager: DialogManager) -> None:
    return await dialog_manager.start(state=AdminRootState.root)
