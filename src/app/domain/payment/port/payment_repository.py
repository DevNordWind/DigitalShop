from abc import ABC, abstractmethod

from app.domain.payment.entity import Payment
from app.domain.payment.value_object import PaymentId


class PaymentRepository(ABC):
    @abstractmethod
    async def add(self, payment: Payment) -> None:
        raise NotImplementedError

    @abstractmethod
    async def acquire(self, payment_id: PaymentId) -> Payment | None:
        raise NotImplementedError
