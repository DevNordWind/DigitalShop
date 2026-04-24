from dataclasses import dataclass

from domain.common.localized import Language
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.setting.position.access_service import (
    PositionSettingsAccessService,
)
from presentation.aiogram.setting.position.exception import (
    PositionSettingsPermissionDenied,
)
from presentation.aiogram.setting.position.model import PositionSettings
from presentation.aiogram.setting.position.port import (
    PositionSettingsGateway,
)


@dataclass(slots=True, frozen=True)
class ChangePositionDefaultLangCmd:
    new_lang: Language


class ChangePositionDefaultLang:
    def __init__(
        self,
        gateway: PositionSettingsGateway,
        ctx: TelegramContextDTO,
    ):
        self._ctx: TelegramContextDTO = ctx
        self._gateway: PositionSettingsGateway = gateway

    async def __call__(self, cmd: ChangePositionDefaultLangCmd) -> None:
        if not PositionSettingsAccessService.can_edit(
            editor_role=self._ctx.user_role,
        ):
            raise PositionSettingsPermissionDenied

        settings: PositionSettings = await self._gateway.get()

        if settings.default_lang == cmd.new_lang:
            return

        settings.default_lang = cmd.new_lang
        await self._gateway.save(settings)
