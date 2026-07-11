from abc import ABC, abstractmethod

from app.app.payment.dto.payment import PaymentDTO
from app.domain.payment.value_object import PaymentId


class PaymentReader(ABC):
    @abstractmethod
    async def read(self, payment_id: PaymentId) -> PaymentDTO | None:
        raise NotImplementedError
