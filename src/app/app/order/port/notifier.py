from abc import ABC, abstractmethod

from app.app.order.dto.order import OrderDTO


class OrderNotifier(ABC):
    @abstractmethod
    async def notify_confirmed(self, order: OrderDTO) -> None:
        raise NotImplementedError
