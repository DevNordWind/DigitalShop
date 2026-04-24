from typing import Any

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from presentation.aiogram.setting.general.model import GeneralBotSettings


@inject
async def info_getter(
    general_settings: FromDishka[GeneralBotSettings], **_: Any
) -> dict[str, Any]:
    return {
        "support_url": getattr(general_settings.support, "url", None),
        "support_username": getattr(
            general_settings.support, "username", None
        ),
        "support_exist": general_settings.support is not None,
    }
