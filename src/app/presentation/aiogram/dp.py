from typing import NamedTuple

from aiogram_dialog import BgManagerFactory, setup_dialogs

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from app.presentation.aiogram.dialog import (
    get_admins_dialogs,
    get_root_dialog,
    get_service_dialogs,
)
from app.presentation.aiogram.dialog.user import get_user_dialogs
from app.presentation.aiogram.filter import IsAdmin
from app.presentation.aiogram.middleware import LoggingContextMiddleware
from app.presentation.aiogram.router import (
    make_command_router,
    make_error_router,
    make_service_router,
)


class DispatcherBundle(NamedTuple):
    dp: Dispatcher
    bg_factory: BgManagerFactory


def make_dispatcher(
    storage: BaseStorage,
    events_isolation: BaseEventIsolation,
) -> DispatcherBundle:
    dp = Dispatcher(storage=storage, events_isolation=events_isolation)
    bg_factory = setup_dialogs(router=dp, events_isolation=events_isolation)
    for observer in dp.observers.values():
        observer.outer_middleware(LoggingContextMiddleware())

    dp.include_routers(*get_service_dialogs())
    dp.include_router(make_service_router())

    dp.include_router(make_command_router())

    dp.include_router(get_root_dialog())
    dp.include_routers(*get_user_dialogs())

    register_admins_dialogs(dp)

    dp.include_router(make_error_router())

    return DispatcherBundle(dp=dp, bg_factory=bg_factory)


def register_admins_dialogs(dp: Dispatcher) -> None:
    dialogs = get_admins_dialogs()
    for dialog in dialogs:
        for observer in dialog.observers.values():
            observer.filter(IsAdmin())

    dp.include_routers(*dialogs)
