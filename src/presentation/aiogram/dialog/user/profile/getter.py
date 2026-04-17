from typing import Any

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.user.dto.report import UserProfileReport
from app.user.query import GetUserProfileReport, GetUserProfileReportQuery
from infra.authentication.telegram.dto import TelegramContextDTO


@inject
async def profile_getter(
    query_handler: FromDishka[GetUserProfileReport],
    tg_ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, Any]:
    report: UserProfileReport = await query_handler(
        GetUserProfileReportQuery(target_identifier=tg_ctx.user_id)
    )
    return {
        "telegram_id": str(tg_ctx.id),
        "orders_count": report.orders_count,
        "top_ups_count": report.top_ups_count,
        "reg_at": report.reg_at,
    }
