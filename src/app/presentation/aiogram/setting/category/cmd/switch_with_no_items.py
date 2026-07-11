from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.presentation.aiogram.setting.category.access_service import (
    CategorySettingsAccessService,
)
from app.presentation.aiogram.setting.category.port import (
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
        CategorySettingsAccessService.ensure_can_edit(
            ctx=self._ctx,
        )

        settings = await self._gateway.get()
        settings.switch_show_with_no_items()

        await self._gateway.save(settings)
