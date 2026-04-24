from typing import Any

from app.common.dto.coefficient import CoefficientDTO
from app.referral.query import GetReferralCoefficient
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from presentation.aiogram.setting.general.model import GeneralBotSettings


@inject
async def general_settings_getter(
    general_settings: FromDishka[GeneralBotSettings],
    query_handler: FromDishka[GetReferralCoefficient],
    **_: Any,
) -> dict[str, Any]:
    referral_coefficient: CoefficientDTO = await query_handler()

    return {
        "tech_work": general_settings.tech_work.status,
        "support_username": general_settings.support.username
        if general_settings.support
        else None,
        "percent": referral_coefficient.as_percent,
    }
