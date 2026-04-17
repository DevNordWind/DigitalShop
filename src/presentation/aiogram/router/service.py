from contextlib import suppress
from uuid import UUID

from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from presentation.aiogram.filter import IsSelectLanguage, IsTechWork
from presentation.aiogram.kb import ServiceKeyboard
from presentation.aiogram.port import Text
from presentation.aiogram.setting.general.model import GeneralBotSettings
from presentation.aiogram.state import (
    OrdersState,
    UnSelectedLangState,
)


def get_service_router() -> Router:
    service_router: Router = Router()

    service_router.callback_query.register(on_close, F.data == "service:close")

    service_router.message.register(on_tech_work_msg, IsTechWork())
    service_router.callback_query.register(on_tech_work_callback, IsTechWork())

    service_router.message.register(on_unselect_lang, ~IsSelectLanguage())
    service_router.callback_query.register(
        on_unselect_lang,
        ~IsSelectLanguage(),
    )
    service_router.callback_query.register(
        on_to_order, F.data.startswith("to_order:")
    )

    return service_router


async def on_close(event: CallbackQuery) -> None:
    with suppress(TelegramAPIError):
        if isinstance(event.message, Message):
            await event.message.delete()


@inject
async def on_tech_work_msg(
    event: Message,
    kb: FromDishka[ServiceKeyboard],
    settings: FromDishka[GeneralBotSettings],
    t: FromDishka[Text],
) -> Message:
    with suppress(TelegramAPIError):
        await event.delete()

    return await event.answer(
        text=t("tech-work"),
        reply_markup=kb.get_tech_work_markup(
            support_url=getattr(settings.support, "url", None)
        ),
    )


@inject
async def on_tech_work_callback(
    event: CallbackQuery,
    kb: FromDishka[ServiceKeyboard],
    settings: FromDishka[GeneralBotSettings],
    t: FromDishka[Text],
) -> Message:
    with suppress(TelegramAPIError):
        if isinstance(event.message, Message):
            await event.message.delete()

    return await event.message.answer(  # type: ignore[union-attr]
        text=t("tech-work"),
        reply_markup=kb.get_tech_work_markup(
            support_url=getattr(settings.support, "url", None)
        ),
    )


async def on_unselect_lang(
    event: Message | CallbackQuery,
    dialog_manager: DialogManager,
) -> None:
    return await dialog_manager.start(state=UnSelectedLangState.select_lang)


async def on_to_order(
    event: CallbackQuery,
    dialog_manager: DialogManager,
) -> None:
    split: list[str] = event.data.split(":")  # type: ignore[union-attr]

    return await dialog_manager.start(
        state=OrdersState.order, data={"order_id": UUID(split[1])}
    )
