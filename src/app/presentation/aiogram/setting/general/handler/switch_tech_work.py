from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.presentation.aiogram.setting.general.access_service import (
    GeneralBotSettingsAccessService,
)
from app.presentation.aiogram.setting.general.model import GeneralBotSettings
from app.presentation.aiogram.setting.general.port import (
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
        GeneralBotSettingsAccessService.ensure_can_edit(
            ctx=self._ctx,
        )

        settings: GeneralBotSettings = await self._gateway.get()
        settings.switch_tech_work_status()

        await self._gateway.save(settings)
