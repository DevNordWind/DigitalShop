from typing import Any

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.app.user.dto import UserProfileDTO
from app.app.user.query import GetUserProfile, GetUserProfileQuery
from app.infra.authentication.telegram.dto import TelegramContextDTO


@inject
async def profile_getter(
    query_handler: FromDishka[GetUserProfile],
    tg_ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, Any]:
    report: UserProfileDTO = await query_handler(
        GetUserProfileQuery(target_identifier=tg_ctx.user_id)
    )
    return {
        "telegram_id": str(tg_ctx.id),
        "orders_count": report.orders_count,
        "top_ups_count": report.top_ups_count,
        "reg_at": report.reg_at,
    }
