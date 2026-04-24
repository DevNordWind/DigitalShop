from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.setting.general.access_service import (
    GeneralBotSettingsAccessService,
)
from presentation.aiogram.setting.general.exception import (
    GeneralBotSettingsPermissionDenied,
)
from presentation.aiogram.setting.general.model import GeneralBotSettings
from presentation.aiogram.setting.general.port import (
    GeneralBotSettingsGateway,
)


class SwitchTechWorkStatus:
    def __init__(
        self,
        ctx: TelegramContextDTO,
        gateway: GeneralBotSettingsGateway,
    ):
        self._ctx: TelegramContextDTO = ctx
        self._gateway: GeneralBotSettingsGateway = gateway

    async def execute(self) -> None:
        if not GeneralBotSettingsAccessService.can_edit(
            editor_role=self._ctx.user_role,
        ):
            raise GeneralBotSettingsPermissionDenied

        settings: GeneralBotSettings = await self._gateway.get()
        settings.tech_work.status = not settings.tech_work.status

        await self._gateway.save(settings)
