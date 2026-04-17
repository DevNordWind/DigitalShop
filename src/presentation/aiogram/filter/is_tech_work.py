from aiogram.filters import Filter
from aiogram.types import TelegramObject
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.setting.general.model import GeneralBotSettings


class IsTechWork(Filter):
    @inject
    async def __call__(
        self,
        event: TelegramObject,
        ctx: FromDishka[TelegramContextDTO],
        settings: FromDishka[GeneralBotSettings],
    ) -> bool:
        if settings.tech_work.status:
            return ctx.user_role not in settings.tech_work.exclude_for

        return False
