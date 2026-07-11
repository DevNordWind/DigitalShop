from dataclasses import dataclass

from app.domain.payment.enums import PaymentMethod
from app.infra.authentication.telegram.dto import TelegramContextDTO
from app.presentation.aiogram.setting.payment.access_service import (
    PaymentSettingsAccessService,
)
from app.presentation.aiogram.setting.payment.port import (
    PaymentSettingsGateway,
)


@dataclass(slots=True, frozen=True)
class SwitchPaymentSettingStatusCmd:
    method: PaymentMethod


class SwitchPaymentSettingStatus:
    def __init__(
        self,
        gateway: PaymentSettingsGateway,
        ctx: TelegramContextDTO,
    ):
        self._gateway: PaymentSettingsGateway = gateway
        self._ctx: TelegramContextDTO = ctx

    async def __call__(self, cmd: SwitchPaymentSettingStatusCmd) -> None:
        PaymentSettingsAccessService.ensure_can_edit(
            ctx=self._ctx,
        )

        settings = await self._gateway.get_by_method(method=cmd.method)
        settings.switch_status()

        await self._gateway.save(settings)
