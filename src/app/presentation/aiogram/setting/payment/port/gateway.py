from abc import ABC, abstractmethod

from app.domain.payment.enums import PaymentMethod
from app.presentation.aiogram.setting.payment.model import PaymentSettings


class PaymentSettingsGateway(ABC):
    @abstractmethod
    async def save(self, settings: PaymentSettings) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self) -> list[PaymentSettings]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_method(self, method: PaymentMethod) -> PaymentSettings:
        raise NotImplementedError
