from abc import ABC, abstractmethod

from app.payment.dto.payment import PaymentDTO
from domain.payment.value_object import PaymentId


class PaymentReader(ABC):
    @abstractmethod
    async def read(self, payment_id: PaymentId) -> PaymentDTO | None:
        raise NotImplementedError
