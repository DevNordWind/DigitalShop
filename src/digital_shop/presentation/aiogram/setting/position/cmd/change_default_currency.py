from dataclasses import dataclass

from domain.common.money import Currency
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
class ChangePositionDefaultCurrencyCmd:
    new_currency: Currency


class ChangePositionDefaultCurrency:
    def __init__(
        self,
        gateway: PositionSettingsGateway,
        ctx: TelegramContextDTO,
    ):
        self._ctx: TelegramContextDTO = ctx
        self._gateway: PositionSettingsGateway = gateway

    async def __call__(self, cmd: ChangePositionDefaultCurrencyCmd) -> None:
        if not PositionSettingsAccessService.can_edit(
            editor_role=self._ctx.user_role,
        ):
            raise PositionSettingsPermissionDenied

        settings: PositionSettings = await self._gateway.get()

        if settings.default_currency == cmd.new_currency:
            return

        settings.default_currency = cmd.new_currency
        await self._gateway.save(settings)
