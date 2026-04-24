from abc import ABC, abstractmethod

from app.payment.port.payment.dto import (
    CancelInvoice,
    CreateInvoice,
    GetInvoice,
    Invoice,
)


class PaymentMethodGateway(ABC):
    @abstractmethod
    async def create(self, data: CreateInvoice) -> Invoice:
        raise NotImplementedError

    @abstractmethod
    async def get(self, data: GetInvoice) -> Invoice:
        raise NotImplementedError

    @abstractmethod
    async def cancel(self, data: CancelInvoice) -> bool:
        raise NotImplementedError
