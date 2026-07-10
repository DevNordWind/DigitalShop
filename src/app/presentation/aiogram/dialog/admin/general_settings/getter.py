from typing import Any

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.app.common.dto.coefficient import CoefficientDTO
from app.app.referral.query import GetReferralCoefficient
from app.presentation.aiogram.setting.general import GeneralBotSettingsGateway


@inject
async def general_settings_getter(
    general_settings_gw: FromDishka[GeneralBotSettingsGateway],
    query_handler: FromDishka[GetReferralCoefficient],
    **_: Any,
) -> dict[str, Any]:
    general_settings = await general_settings_gw.get()
    referral_coefficient: CoefficientDTO = await query_handler()

    return {
        "tech_work": general_settings.tech_work.status,
        "support_username": general_settings.support.username
        if general_settings.support
        else None,
        "percent": referral_coefficient.as_percent,
    }
