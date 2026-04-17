from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.setting.category.access_service import (
    CategorySettingsAccessService,
)
from presentation.aiogram.setting.category.exception import (
    CategorySettingsPermissionDenied,
)
from presentation.aiogram.setting.category.model import CategorySettings
from presentation.aiogram.setting.category.port import (
    CategorySettingsGateway,
)


class SwitchWithNoItemsCategory:
    def __init__(
        self,
        gateway: CategorySettingsGateway,
        ctx: TelegramContextDTO,
    ):
        self._ctx: TelegramContextDTO = ctx
        self._gateway: CategorySettingsGateway = gateway

    async def __call__(self) -> None:
        if not CategorySettingsAccessService.can_edit(
            editor_role=self._ctx.user_role,
        ):
            raise CategorySettingsPermissionDenied

        settings: CategorySettings = await self._gateway.get()
        settings.show_with_no_items = not settings.show_with_no_items

        await self._gateway.save(settings)
