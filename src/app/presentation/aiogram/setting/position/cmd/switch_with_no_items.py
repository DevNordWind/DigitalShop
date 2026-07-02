from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.presentation.aiogram.setting.position.access_service import (
    PositionSettingsAccessService,
)
from app.presentation.aiogram.setting.position.model import PositionSettings
from app.presentation.aiogram.setting.position.port import (
    PositionSettingsGateway,
)


class SwitchShowPositionWithNoItems:
    def __init__(
        self,
        gateway: PositionSettingsGateway,
        ctx: TelegramContextDTO,
    ):
        self._ctx: TelegramContextDTO = ctx
        self._gateway: PositionSettingsGateway = gateway

    async def __call__(self) -> None:
        PositionSettingsAccessService.ensure_can_edit(
            ctx=self._ctx,
        )

        settings: PositionSettings = await self._gateway.get()
        settings.switch_show_with_no_items()

        await self._gateway.save(settings)
