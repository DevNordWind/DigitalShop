from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.app.common.dto.query_params import SortingOrder
from app.app.referral.cmd import (
    ChangeReferrerProfileAwardCurrency,
    ChangeReferrerProfileAwardCurrencyCmd,
    SwitchReferrerProfileNotifications,
)
from app.app.referral.cmd.switch_send_notifications import (
    SwitchReferrerProfileNotificationsCmd,
)
from app.domain.common.money import Currency
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.presentation.aiogram.dialog.user.profile.referral.ctx import (
    CTX_KEY,
    ReferralCtx,
    TimeUnit,
)
from app.presentation.aiogram.state import ReferralState


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx = ReferralCtx(current_sorting_order=SortingOrder.DESC)
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_time_unit(
    event: CallbackQuery,
    widget: Select[TimeUnit | None],
    dialog_manager: DialogManager,
    unit: TimeUnit | None,
    retort: FromDishka[Retort],
) -> None:
    ctx: ReferralCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ReferralCtx,
    )
    if ctx.current_time_unit == unit:
        return

    ctx.current_time_unit = unit

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_switch_send_notifications(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    handler: FromDishka[SwitchReferrerProfileNotifications],
    tg_ctx: FromDishka[TelegramContextDTO],
) -> None:
    await handler(SwitchReferrerProfileNotificationsCmd(target_user_id=tg_ctx.user_id))


@inject
async def on_select_award(
    event: CallbackQuery,
    widget: Select[UUID],
    dialog_manager: DialogManager,
    award_id: UUID,
    retort: FromDishka[Retort],
) -> None:
    ctx: ReferralCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ReferralCtx,
    )
    ctx.current_award_id = award_id

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
    await dialog_manager.switch_to(state=ReferralState.my_award)


@inject
async def on_sorting_order(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: ReferralCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ReferralCtx,
    )
    ctx.current_sorting_order = (
        SortingOrder.DESC
        if ctx.current_sorting_order == SortingOrder.ASC
        else SortingOrder.ASC
    )

    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_change_currency(
    event: CallbackQuery,
    widget: Select[Currency],
    dialog_manager: DialogManager,
    new_currency: Currency,
    handler: FromDishka[ChangeReferrerProfileAwardCurrency],
    tg_ctx: FromDishka[TelegramContextDTO],
) -> None:
    await handler(
        ChangeReferrerProfileAwardCurrencyCmd(
            new_currency=new_currency, user_id=tg_ctx.user_id
        ),
    )
