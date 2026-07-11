from dataclasses import dataclass

from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.presentation.aiogram.setting.general.access_service import (
    GeneralBotSettingsAccessService,
)
from app.presentation.aiogram.setting.general.model import (
    GeneralBotSettings,
    SupportContact,
)
from app.presentation.aiogram.setting.general.port import (
    GeneralBotSettingsGateway,
)


@dataclass(slots=True, frozen=True)
class SetSupportUsernameCmd:
    username: str


class SetSupportUsername:
    def __init__(
        self,
        ctx: TelegramContextDTO,
        gateway: GeneralBotSettingsGateway,
    ):
        self._ctx: TelegramContextDTO = ctx
        self._gateway: GeneralBotSettingsGateway = gateway

    async def execute(self, cmd: SetSupportUsernameCmd) -> None:
        GeneralBotSettingsAccessService.ensure_can_edit(
            ctx=self._ctx,
        )

        settings: GeneralBotSettings = await self._gateway.get()
        settings.set_support(support=SupportContact(username=cmd.username))

        await self._gateway.save(settings)
