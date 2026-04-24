from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram_dialog import setup_dialogs
from presentation.aiogram.dialog import (
    get_admins_dialogs,
    get_root_dialog,
    get_service_dialogs,
)
from presentation.aiogram.dialog.user import get_user_dialogs
from presentation.aiogram.filter import IsAdmin
from presentation.aiogram.router import (
    get_command_router,
    get_error_router,
    get_service_router,
)


def get_dispatcher(
    storage: BaseStorage,
    events_isolation: BaseEventIsolation,
) -> Dispatcher:
    dp = Dispatcher(storage=storage, events_isolation=events_isolation)
    setup_dialogs(router=dp)

    dp.include_routers(*get_service_dialogs())
    dp.include_router(get_service_router())

    dp.include_router(get_command_router())

    dp.include_router(get_root_dialog())
    dp.include_routers(*get_user_dialogs())

    register_admins_dialogs(dp)

    dp.include_router(get_error_router())

    return dp


def register_admins_dialogs(dp: Dispatcher) -> None:
    dialogs = get_admins_dialogs()
    for dialog in dialogs:
        for observer in dialog.observers.values():
            observer.filter(IsAdmin())

    dp.include_routers(*dialogs)
