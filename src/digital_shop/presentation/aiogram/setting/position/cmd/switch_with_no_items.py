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


class SwitchShowPositionWithNoItems:
    def __init__(
        self,
        gateway: PositionSettingsGateway,
        ctx: TelegramContextDTO,
    ):
        self._ctx: TelegramContextDTO = ctx
        self._gateway: PositionSettingsGateway = gateway

    async def __call__(self) -> None:
        if not PositionSettingsAccessService.can_edit(
            editor_role=self._ctx.user_role,
        ):
            raise PositionSettingsPermissionDenied

        settings: PositionSettings = await self._gateway.get()

        settings.show_with_no_items = not settings.show_with_no_items
        await self._gateway.save(settings)
