from abc import ABC, abstractmethod

from domain.payment.entity import Payment
from domain.payment.value_object import PaymentId


class PaymentRepository(ABC):
    @abstractmethod
    async def add(self, payment: Payment) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, payment_id: PaymentId) -> Payment | None:
        raise NotImplementedError
