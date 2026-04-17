from typing import Any

from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from domain.user.enums import UserRole
from infra.authentication.telegram.dto import TelegramContextDTO


@inject
async def root_getter(
    ctx: FromDishka[TelegramContextDTO],
    **_: Any,
) -> dict[str, UserRole]:
    return {"user_role": ctx.user_role}
