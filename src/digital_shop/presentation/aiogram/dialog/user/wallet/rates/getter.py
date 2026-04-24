from dataclasses import dataclass
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from domain.common.exchange_rate import (
    CurrencyPair,
    ExchangeRate,
    ExchangeRateGateway,
)
from domain.common.money import Currency
from presentation.aiogram.port import Text

from .ctx import BASE_CURRENCY, CTX_KEY, CurrencyRatesCtx


@dataclass(slots=True, frozen=True)
class CurrencyButton:
    currency: Currency

    is_current: bool


@inject
async def rates_getter(
    rate_gateway: FromDishka[ExchangeRateGateway],
    text: FromDishka[Text],
    **_: Any,
) -> dict[str, Any]:
    pairs: list[CurrencyPair] = [
        CurrencyPair(source=BASE_CURRENCY, target=currency)
        for currency in Currency
        if currency != BASE_CURRENCY
    ]
    rates: list[ExchangeRate] = await rate_gateway.get_many(pairs=pairs)
    rows: list[str] = [
        text(
            "rate-row",
            source_currency=rate.pair.source,
            target_currency=rate.pair.target,
            rate_amount=rate.rate,
        )
        for rate in rates
    ]

    return {"rate_rows": "\n".join(rows)}


@inject
async def related_rates_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    rate_gw: FromDishka[ExchangeRateGateway],
    text: FromDishka[Text],
    **_: Any,
) -> dict[str, Any]:
    ctx: CurrencyRatesCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], CurrencyRatesCtx
    )
    source_buttons: list[CurrencyButton] = [
        CurrencyButton(
            currency=currency,
            is_current=currency == ctx.related_source_currency,
        )
        for currency in Currency
    ]
    target_buttons: list[CurrencyButton] = [
        CurrencyButton(
            currency=currency,
            is_current=currency == ctx.related_target_currency,
        )
        for currency in Currency
    ]

    if (
        ctx.related_source_currency is None
        or ctx.related_target_currency is None
    ):
        return {
            "is_rate_ready": False,
            "source_buttons": source_buttons,
            "target_buttons": target_buttons,
        }

    rate: ExchangeRate = await rate_gw.get(
        pair=CurrencyPair(
            source=ctx.related_source_currency,
            target=ctx.related_target_currency,
        )
    )

    return {
        "is_rate_ready": True,
        "source_currency": rate.pair.source,
        "target_currency": rate.pair.target,
        "rate_amount": rate.rate,
        "source_buttons": source_buttons,
        "target_buttons": target_buttons,
    }
