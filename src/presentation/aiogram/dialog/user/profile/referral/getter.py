from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from adaptix import Retort
from aiogram import Bot
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.common.dto.coefficient import CoefficientDTO
from app.common.dto.period import TimePeriod
from app.common.dto.query_params import OffsetPaginationParams
from app.referral.dto.award import ReferralAwardDTO
from app.referral.dto.paginated import ReferralAwardsPaginated
from app.referral.dto.profile import ReferrerProfileDTO
from app.referral.dto.report import ConvertedReferrerReport
from app.referral.dto.sorting import ReferralAwardSortingParams
from app.referral.query import (
    GetMyReferralAwards,
    GetMyReferralAwardsQuery,
    GetMyReferrerReport,
    GetMyReferrerReportQuery,
    GetReferralAward,
    GetReferralAwardQuery,
    GetReferralCoefficient,
)
from app.referral.query.get_my_profile import GetMyReferrerProfile
from domain.common.money import Currency
from domain.referral.enums.status import ReferralAwardStatus
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.dialog.user.profile.referral.ctx import (
    AWARDS_HEIGHT,
    AWARDS_SCROLL,
    CTX_KEY,
    ReferralCtx,
    TimeUnit,
)
from presentation.aiogram.referral import create_ref_deeplink


@dataclass(slots=True, frozen=True)
class TimeUnitButton:
    unit: TimeUnit | None

    is_current: bool


@dataclass(slots=True, frozen=True)
class ReferralAwardButton:
    id: UUID

    amount: Decimal | None
    currency: Currency | None

    status: ReferralAwardStatus
    created_at: datetime


@dataclass(slots=True, frozen=True)
class CurrencyButton:
    currency: Currency

    is_current: bool


@inject
async def referral_getter(
    dialog_manager: DialogManager,
    bot: Bot,
    retort: FromDishka[Retort],
    profile_handler: FromDishka[GetMyReferrerProfile],
    report_handler: FromDishka[GetMyReferrerReport],
    coefficient_handler: FromDishka[GetReferralCoefficient],
    tg_ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, Any]:
    ctx: ReferralCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ReferralCtx,
    )
    coefficient: CoefficientDTO = await coefficient_handler()

    profile: ReferrerProfileDTO | None = await profile_handler()
    if not profile:
        return {"is_referrer": False, "percent": coefficient.as_percent}

    period: TimePeriod | None = None
    if ctx.current_time_unit is not None:
        now = datetime.now(UTC)
        period = TimePeriod(
            from_date=ctx.current_time_unit.calculate_from(
                now=now,
            ),
            to_date=now,
        )

    report: ConvertedReferrerReport = await report_handler(
        GetMyReferrerReportQuery(
            convert_to=profile.award_currency,
            period=period,
        ),
    )

    link: str = await create_ref_deeplink(bot=bot, tg_user_id=tg_ctx.id)

    return {
        "is_referrer": True,
        "percent": coefficient.as_percent,
        "referral_count": report.report.referral_count,
        "awards_count": report.report.awards_count,
        "total_amount": report.total.amount,
        "currency": report.total.currency,
        "send_notifications": profile.send_notifications,
        "link": link,
        "buttons": [
            TimeUnitButton(
                unit=None, is_current=ctx.current_time_unit is None
            ),
        ]
        + [
            TimeUnitButton(unit=unit, is_current=unit == ctx.current_time_unit)
            for unit in TimeUnit
        ],
    }


@inject
async def my_awards_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetMyReferralAwards],
    **_: Any,
) -> dict[str, Any]:
    ctx: ReferralCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ReferralCtx,
    )
    current_page: int = await dialog_manager.find(AWARDS_SCROLL).get_page()  # type: ignore[union-attr]

    offset = AWARDS_HEIGHT * current_page
    paginated: ReferralAwardsPaginated = await query_handler(
        GetMyReferralAwardsQuery(
            sorting=ReferralAwardSortingParams(
                field="created_at",
                order=ctx.current_sorting_order,
            ),
            pagination=OffsetPaginationParams(
                offset=offset,
                limit=AWARDS_HEIGHT,
            ),
        ),
    )

    return {
        "pages": (paginated.total + AWARDS_HEIGHT - 1) // AWARDS_HEIGHT,
        "buttons": [
            ReferralAwardButton(
                id=award.id,
                amount=award.award.amount if award.award else None,
                currency=award.award.currency if award.award else None,
                status=award.status,
                created_at=award.created_at,
            )
            for award in paginated.awards
        ],
        "sorting_order": ctx.current_sorting_order,
    }


@inject
async def my_award_getter(
    dialog_manager: DialogManager,
    retort: FromDishka[Retort],
    query_handler: FromDishka[GetReferralAward],
    **_: Any,
) -> dict[str, Any]:
    ctx: ReferralCtx = retort.load(
        dialog_manager.dialog_data[CTX_KEY],
        ReferralCtx,
    )
    if ctx.current_award_id is None:
        return {}

    award: ReferralAwardDTO = await query_handler(
        GetReferralAwardQuery(id=ctx.current_award_id),
    )

    return {
        "amount": award.award.amount if award.award else None,
        "currency": award.award.currency if award.award else None,
        "completed_at": award.completed_at,
        "created_at": award.created_at,
        "status": award.status,
    }


@inject
async def change_currency_getter(
    query_handler: FromDishka[GetMyReferrerProfile],
    **_: Any,
) -> dict[str, Any]:
    profile = await query_handler()
    if profile is None:
        return {}

    return {
        "buttons": [
            CurrencyButton(
                currency=currency,
                is_current=profile.award_currency == currency,
            )
            for currency in Currency
        ],
    }
