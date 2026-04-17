from typing import Protocol

from domain.payment.enums import PaymentMethod
from presentation.aiogram.setting.payment.model import PaymentSettings


class PaymentSettingsGateway(Protocol):
    async def save(self, settings: PaymentSettings) -> None:
        raise NotImplementedError

    async def get(self) -> list[PaymentSettings]:
        raise NotImplementedError

    async def get_by_method(self, method: PaymentMethod) -> PaymentSettings:
        raise NotImplementedError
