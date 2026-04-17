from aiogram.filters import Filter
from aiogram.types import TelegramObject
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from infra.authentication.telegram.dto import TelegramContextDTO


class IsSelectLanguage(Filter):
    @inject
    async def __call__(
        self,
        event: TelegramObject,
        ctx: FromDishka[TelegramContextDTO],
    ) -> bool:
        return ctx.lang is not None
