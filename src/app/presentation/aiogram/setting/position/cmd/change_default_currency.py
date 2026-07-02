from dataclasses import dataclass

from app.domain.common.money import Currency
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.presentation.aiogram.setting.position.access_service import (
    PositionSettingsAccessService,
)
from app.presentation.aiogram.setting.position.model import PositionSettings
from app.presentation.aiogram.setting.position.port import (
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
        self._ctx = ctx
        self._gateway = gateway

    async def __call__(self, cmd: ChangePositionDefaultCurrencyCmd) -> None:
        PositionSettingsAccessService.ensure_can_edit(ctx=self._ctx)
        settings: PositionSettings = await self._gateway.get()

        if settings.default_currency == cmd.new_currency:
            return

        settings.default_currency = cmd.new_currency
        await self._gateway.save(settings)
