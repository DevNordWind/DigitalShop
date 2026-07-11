from dishka import FromDishka
from dishka.integrations.aiogram import inject

from aiogram.filters import Filter
from aiogram.types import TelegramObject
from app.domain.user.enums import UserRole
from app.infra.authentication.telegram.dto import TelegramContextDTO


class IsAdmin(Filter):
    @inject
    async def __call__(
        self,
        event: TelegramObject,
        ctx: FromDishka[TelegramContextDTO],
    ) -> bool:
        return ctx.user_role >= UserRole.ADMIN
