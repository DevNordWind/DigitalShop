from dataclasses import dataclass

from app.domain.common.localized import Language
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.presentation.aiogram.setting.category.access_service import (
    CategorySettingsAccessService,
)
from app.presentation.aiogram.setting.category.port import (
    CategorySettingsGateway,
)


@dataclass(slots=True, frozen=True)
class ChangeCategoryDefaultLangCmd:
    new_lang: Language


class ChangeCategoryDefaultLang:
    def __init__(
        self,
        gateway: CategorySettingsGateway,
        ctx: TelegramContextDTO,
    ):
        self._ctx = ctx
        self._gateway = gateway

    async def __call__(self, cmd: ChangeCategoryDefaultLangCmd) -> None:
        CategorySettingsAccessService.ensure_can_edit(
            ctx=self._ctx,
        )

        settings = await self._gateway.get()

        if settings.default_lang == cmd.new_lang:
            return

        settings.default_lang = cmd.new_lang

        await self._gateway.save(settings)
