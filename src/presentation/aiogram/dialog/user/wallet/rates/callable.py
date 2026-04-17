from typing import Any

from adaptix import Retort
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from domain.common.money import Currency
from presentation.aiogram.dialog.user.wallet.rates.ctx import (
    CTX_KEY,
    CurrencyRatesCtx,
)


@inject
async def on_start(
    data: Any,
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
) -> None:
    ctx = CurrencyRatesCtx()
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_source(
    event: CallbackQuery,
    widget: Select[Currency],
    dialog_manager: DialogManager,
    currency: Currency,
    retort: FromDishka[Retort],
) -> None:
    ctx: CurrencyRatesCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], CurrencyRatesCtx
    )
    if ctx.related_target_currency == currency:
        return
    ctx.related_source_currency = currency
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)


@inject
async def on_select_target(
    event: CallbackQuery,
    widget: Select[Currency],
    dialog_manager: DialogManager,
    currency: Currency,
    retort: FromDishka[Retort],
) -> None:
    ctx: CurrencyRatesCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], CurrencyRatesCtx
    )
    if ctx.related_source_currency == currency:
        return

    ctx.related_target_currency = currency
    dialog_manager.dialog_data[CTX_KEY] = retort.dump(ctx)
