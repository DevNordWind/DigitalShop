from typing import Any

from adaptix import Retort
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import AsyncContainer, FromDishka
from dishka.integrations.aiogram_dialog import inject

from domain.common.money import Currency
from infra.authentication.telegram.handler import (
    UpdateTelegramCurrency,
    UpdateTelegramCurrencyCmd,
)
from presentation.aiogram.dialog.user.wallet.ctx import CTX_KEY, WalletCtx


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx = WalletCtx()
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_switch_show_all_balances(
    event: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx: WalletCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        WalletCtx,
    )
    ctx.show_all_balances = not ctx.show_all_balances
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_change_wallet(
    event: CallbackQuery,
    widget: Select[Currency],
    dialog_manager: DialogManager,
    currency: Currency,
    handler: FromDishka[UpdateTelegramCurrency],
    container: FromDishka[AsyncContainer],
) -> None:
    await handler.execute(UpdateTelegramCurrencyCmd(new_currency=currency))
    await container.close()
