from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.order.entity import Order
from app.domain.order.value_object import OrderId


class OrderRepository(ABC):
    @abstractmethod
    async def add(self, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, order_id: OrderId) -> Order | None:
        raise NotImplementedError

    @abstractmethod
    async def acquire(self, order_id: OrderId) -> Order | None:
        raise NotImplementedError

    @abstractmethod
    async def get_expired(self, now: datetime, ttl_seconds: int) -> list[Order]:
        raise NotImplementedError
