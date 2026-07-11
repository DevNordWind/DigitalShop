from abc import ABC, abstractmethod

from app.app.payment.port.payment.gateway import PaymentMethodGateway
from app.domain.payment.enums import PaymentMethod


class PaymentMethodGatewayFactory(ABC):
    @abstractmethod
    async def get(self, method: PaymentMethod) -> PaymentMethodGateway:
        raise NotImplementedError
