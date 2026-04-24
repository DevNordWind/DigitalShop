from dataclasses import dataclass

from domain.common.localized import Language
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.setting.category.access_service import (
    CategorySettingsAccessService,
)
from presentation.aiogram.setting.category.exception import (
    CategorySettingsPermissionDenied,
)
from presentation.aiogram.setting.category.port import (
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
        self._ctx: TelegramContextDTO = ctx
        self._gateway: CategorySettingsGateway = gateway

    async def __call__(self, cmd: ChangeCategoryDefaultLangCmd) -> None:
        if not CategorySettingsAccessService.can_edit(
            editor_role=self._ctx.user_role,
        ):
            raise CategorySettingsPermissionDenied

        settings = await self._gateway.get()

        if settings.default_lang == cmd.new_lang:
            return

        settings.default_lang = cmd.new_lang

        await self._gateway.save(settings)
