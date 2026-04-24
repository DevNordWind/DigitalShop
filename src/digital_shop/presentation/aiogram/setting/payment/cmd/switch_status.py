from dataclasses import dataclass

from domain.payment.enums import PaymentMethod
from infra.authentication.telegram.dto import TelegramContextDTO
from presentation.aiogram.setting.payment.access_service import (
    PaymentSettingsAccessService,
)
from presentation.aiogram.setting.payment.exception import (
    PaymentSettingsPermissionDenied,
)
from presentation.aiogram.setting.payment.port import (
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
        if not PaymentSettingsAccessService.can_edit(
            editor_role=self._ctx.user_role,
        ):
            raise PaymentSettingsPermissionDenied

        settings = await self._gateway.get_by_method(method=cmd.method)
        settings.is_active = not settings.is_active

        await self._gateway.save(settings)
