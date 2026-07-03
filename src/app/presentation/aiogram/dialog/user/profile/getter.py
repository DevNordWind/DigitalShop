from typing import Any

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.app.user.dto import UserProfileDTO
from app.app.user.query import GetUserProfile, GetUserProfileQuery
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.presentation.aiogram.util.timezone_processor import TimeZoneProcessor


@inject
async def profile_getter(
    query_handler: FromDishka[GetUserProfile],
    tg_ctx: FromDishka[TelegramContextDTO],
    timezone_processor: FromDishka[TimeZoneProcessor],
    **_: Any,
) -> dict[str, Any]:
    profile: UserProfileDTO = await query_handler(
        GetUserProfileQuery(target_identifier=tg_ctx.user_id)
    )
    return {
        "telegram_id": str(tg_ctx.id),
        "orders_count": profile.orders_count,
        "top_ups_count": profile.top_ups_count,
        "reg_at": timezone_processor.process(dt=profile.reg_at),
    }
