from abc import ABC, abstractmethod
from uuid import UUID

from app.app.common.dto.query_params import OffsetPaginationParams, SortingOrder
from app.app.shopping.position.dto.item import ItemDTO, ItemStatus
from app.app.shopping.position.dto.paginated import PositionItemsPaginated
from app.domain.shopping.position.value_object import PositionId


class PositionItemReader(ABC):
    @abstractmethod
    async def read(self, item_id: UUID) -> ItemDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def read_by_position_id(
        self,
        position_id: PositionId,
        sorting_order: SortingOrder,
        pagination: OffsetPaginationParams,
        status: ItemStatus | None,
    ) -> PositionItemsPaginated:
        raise NotImplementedError
