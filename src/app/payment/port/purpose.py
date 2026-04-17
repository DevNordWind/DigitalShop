from abc import ABC, abstractmethod

from app.payment.dto.payment import PaymentDTO
from domain.payment.enums import PaymentPurposeType


class PaymentPurposeHandler(ABC):
    @abstractmethod
    async def __call__(self, payment: PaymentDTO) -> None:
        raise NotImplementedError


class PaymentPurposeHandlersRegistry(ABC):
    @abstractmethod
    async def get(
        self,
        purpose_type: PaymentPurposeType,
    ) -> PaymentPurposeHandler | None:
        raise NotImplementedError
