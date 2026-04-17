from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from adaptix import Retort
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.period import TimePeriod
from app.report.dto.general_report import ConvertedGeneralReport
from app.report.query import (
    GetConvertedGeneralReport,
    GetConvertedGeneralReportQuery,
)
from domain.common.money import Currency
from presentation.aiogram.dialog.admin.statistic.ctx import (
    CTX_KEY,
    AdminStatisticCtx,
    PeriodUnit,
)
from presentation.aiogram.port import Text


@dataclass(slots=True, frozen=True)
class PeriodUnitButton:
    unit: PeriodUnit | None

    is_current: bool


@dataclass(slots=True, frozen=True)
class CurrencyButton:
    currency: Currency

    is_current: bool


@inject
async def statistic_getter(
    dialog_manager: DialogManager,
    query_handler: FromDishka[GetConvertedGeneralReport],
    retort: FromDishka[Retort],
    t: FromDishka[Text],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminStatisticCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], AdminStatisticCtx
    )
    now: datetime = datetime.now(UTC)
    time_period: TimePeriod | None = ctx.calculate_period(now=now)

    report: ConvertedGeneralReport = await query_handler(
        GetConvertedGeneralReportQuery(
            period=time_period, convert_to=ctx.convert_to
        )
    )
    buttons: list[PeriodUnitButton] = [
        PeriodUnitButton(
            unit=None,
            is_current=ctx.period_unit is None and ctx.custom_period is None,
        )
    ]
    buttons.extend(
        [
            PeriodUnitButton(
                unit=unit,
                is_current=ctx.period_unit == unit
                and ctx.custom_period is None,
            )
            for unit in PeriodUnit
        ]
    )

    return {
        "sales": t(
            "admin-statistic-sales",
            count=report.sales.count,
            amount=report.sales.amount.amount,
            currency=report.sales.amount.currency,
        ),
        "top_ups": t(
            "admin-statistic-top-ups",
            count=report.top_ups.count,
            amount=report.top_ups.amount.amount,
            currency=report.top_ups.amount.currency,
        ),
        "new_users": report.new_users,
        "category_count": report.products.category_count,
        "position_count": report.products.position_count,
        "items_count": report.products.items_count,
        "has_period": time_period is not None,
        "from_date": getattr(time_period, "from_date", None),
        "to_date": getattr(time_period, "to_date", None),
        "buttons": buttons,
    }


@inject
async def input_period_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminStatisticCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], AdminStatisticCtx
    )
    now: datetime = datetime.now(UTC)
    time_period: TimePeriod | None = ctx.calculate_period(now=now)

    return {
        "has_custom_period": ctx.custom_period is not None,
        "from_date": getattr(time_period, "from_date", None),
        "to_date": getattr(time_period, "to_date", None),
    }


@inject
async def convert_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    **_: Any,
) -> dict[str, Any]:
    ctx: AdminStatisticCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY], AdminStatisticCtx
    )

    return {
        "buttons": [
            CurrencyButton(
                currency=currency, is_current=ctx.convert_to == currency
            )
            for currency in Currency
        ]
    }
