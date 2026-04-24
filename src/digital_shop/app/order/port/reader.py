from abc import ABC, abstractmethod

from app.common.dto.query_params import OffsetPaginationParams
from app.order.dto.order import OrderDTO
from app.order.dto.paginated import OrdersPaginatedByReader
from app.order.dto.sorting import OrderSortingParams
from domain.order.enums import OrderStatus
from domain.order.value_object import OrderId
from domain.user.value_object import UserId


class OrderReader(ABC):
    @abstractmethod
    async def read_by_id(self, order_id: OrderId) -> OrderDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def read_by_customer_id(
        self,
        customer_id: UserId,
        sorting: OrderSortingParams,
        pagination: OffsetPaginationParams,
        status: OrderStatus | None,
    ) -> OrdersPaginatedByReader:
        raise NotImplementedError
