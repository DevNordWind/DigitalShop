from dataclasses import dataclass
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.money import Currency
from domain.payment.enums import PaymentMethod
from presentation.aiogram.dialog.user.wallet.top_up.ctx import (
    CTX_KEY,
    TopUpCtx,
)
from presentation.aiogram.setting.payment.port import (
    PaymentSettingsGateway,
)


@dataclass(slots=True, frozen=True)
class PaymentMethodButton:
    method: PaymentMethod


@dataclass(slots=True, frozen=True)
class CurrencyButton:
    currency: Currency

    is_current: bool


@inject
async def input_amount_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: TopUpCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], TopUpCtx)
    return {"currency": ctx.current_currency}


@inject
async def select_payment_method_getter(
    settings_gateway: FromDishka[PaymentSettingsGateway],
    **_: Any,
) -> dict[str, Any]:
    settings = await settings_gateway.get()

    return {
        "buttons": [
            PaymentMethodButton(method=setting.method)
            for setting in settings
            if setting.is_active
        ],
    }


@inject
async def payment_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: TopUpCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], TopUpCtx)
    if ctx.invoice is None:
        return {}

    return {
        "payment_id": ctx.invoice.payment_id,
        "amount": ctx.invoice.to_pay.amount,
        "currency": ctx.invoice.to_pay.currency,
        "method": ctx.invoice.payment_method,
        "invoice_url": ctx.invoice.pay_url,
    }


@inject
async def select_currency_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: TopUpCtx = retort.load(dialog_manager.dialog_data[CTX_KEY], TopUpCtx)
    return {
        "buttons": [
            CurrencyButton(
                currency=currency,
                is_current=ctx.current_currency == currency,
            )
            for currency in Currency
        ],
    }
