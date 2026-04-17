from dataclasses import dataclass

from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.setting.general.access_service import (
    GeneralBotSettingsAccessService,
)
from presentation.aiogram.setting.general.exception import (
    GeneralBotSettingsPermissionDenied,
)
from presentation.aiogram.setting.general.model import (
    GeneralBotSettings,
    SupportContact,
)
from presentation.aiogram.setting.general.port import (
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
        if not GeneralBotSettingsAccessService.can_edit(
            editor_role=self._ctx.user_role,
        ):
            raise GeneralBotSettingsPermissionDenied

        settings: GeneralBotSettings = await self._gateway.get()
        settings.support = SupportContact(username=cmd.username)

        await self._gateway.save(settings)
