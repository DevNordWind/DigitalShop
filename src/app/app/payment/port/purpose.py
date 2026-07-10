from abc import ABC, abstractmethod

from app.app.payment.dto.payment import PaymentDTO
from app.domain.payment.enums import PaymentPurposeType


class PaymentPurposeHandler(ABC):
    @abstractmethod
    async def apply(self, payment: PaymentDTO) -> None:
        """Execute business logic"""
        raise NotImplementedError

    @abstractmethod
    async def notify(self, payment: PaymentDTO) -> None:
        raise NotImplementedError


class PaymentPurposeHandlersRegistry(ABC):
    @abstractmethod
    async def get(
        self,
        purpose_type: PaymentPurposeType,
    ) -> PaymentPurposeHandler:
        raise NotImplementedError
