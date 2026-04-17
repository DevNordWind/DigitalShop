from datetime import datetime

from adaptix import Retort
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Data, DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.period import TimePeriod
from domain.common.money import Currency
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.admin.statistic.ctx import (
    CTX_KEY,
    AdminStatisticCtx,
    PeriodUnit,
)
from presentation.aiogram.port import Text
from presentation.aiogram.state import AdminStatisticState


def map_period_unit(value: str) -> PeriodUnit | None:
    if value == "None":
        return None
    return PeriodUnit(value)


def map_period(value: str) -> tuple[datetime, datetime]:
    split = value.split("-")
    from_date = datetime.strptime(split[0].strip(), "%d.%m.%y").astimezone()
    to_date = datetime.strptime(split[1].strip(), "%d.%m.%y").astimezone()

    return from_date, to_date


@inject
async def on_start(
    _: Data,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    tg_ctx: FromDishka[TelegramContextDTO],
) -> None:
    ctx = AdminStatisticCtx(convert_to=tg_ctx.currency)
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_input_period(
    event: Message,
    widget: ManagedTextInput[tuple[datetime, datetime]],
    dialog_manager: DialogManager,
    time_period: tuple[datetime, datetime],
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminStatisticCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], AdminStatisticCtx
    )
    ctx.custom_period = TimePeriod(
        from_date=time_period[0], to_date=time_period[1]
    )
    await event.delete()
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)

    await dialog_manager.switch_to(
        state=AdminStatisticState.statistic, show_mode=ShowMode.EDIT
    )


@inject
async def on_input_period_error(
    event: Message,
    widget: ManagedTextInput[tuple[datetime, datetime]],
    dialog_manager: DialogManager,
    error: ValueError,
    t: FromDishka[Text],
) -> Message:
    return await event.reply(text=t("admin-statistic-period.invalid"))


@inject
async def on_select_currency(
    event: CallbackQuery,
    widget: Select[Currency],
    dialog_manager: DialogManager,
    currency: Currency,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminStatisticCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], AdminStatisticCtx
    )
    if ctx.convert_to == currency:
        return

    ctx.convert_to = currency
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_period(
    event: CallbackQuery,
    widget: Select[PeriodUnit],
    dialog_manager: DialogManager,
    unit: PeriodUnit,
    retort: FromDishka[Retort],
) -> None:
    ctx: AdminStatisticCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], AdminStatisticCtx
    )
    ctx.period_unit = unit

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
