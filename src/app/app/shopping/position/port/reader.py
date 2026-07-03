from abc import ABC, abstractmethod
from uuid import UUID

from app.app.common.dto.query_params import OffsetPaginationParams
from app.app.shopping.position.dto.item import ItemDTO, ItemStatus
from app.app.shopping.position.dto.paginated import (
    PositionItemsPaginated,
    PositionsPaginated,
    PositionsShortPaginated,
    PositionWithItemsAmountPaginated,
)
from app.app.shopping.position.dto.position import (
    PositionDTO,
    PositionShortDTO,
    PositionWithItemsAmount,
)
from app.app.shopping.position.dto.sorting import (
    PositionItemsSortingParams,
    PositionSortingParams,
)
from app.domain.shopping.category.value_object import CategoryId
from app.domain.shopping.position.enums import PositionStatus
from app.domain.shopping.position.value_object import PositionId


class PositionReader(ABC):
    @abstractmethod
    async def read(self, position_id: PositionId) -> PositionDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def read_short(
        self,
        position_id: PositionId,
    ) -> PositionShortDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def read_with_items_amount(
        self, position_id: PositionId, item_status: ItemStatus | None = None
    ) -> PositionWithItemsAmount | None:
        raise NotImplementedError

    @abstractmethod
    async def read_short_by_category_id(
        self,
        category_id: CategoryId,
        sorting: PositionSortingParams,
        pagination: OffsetPaginationParams,
        show_with_no_items: bool | None,
        status: PositionStatus | None,
    ) -> PositionsShortPaginated:
        raise NotImplementedError

    @abstractmethod
    async def read_all_by_category_id(
        self,
        category_id: CategoryId,
        sorting: PositionSortingParams,
        pagination: OffsetPaginationParams,
        status: PositionStatus | None,
        show_with_no_items: bool | None,
    ) -> PositionsPaginated:
        raise NotImplementedError

    @abstractmethod
    async def read_with_items_amount_by_category_id(
        self,
        category_id: CategoryId,
        sorting: PositionSortingParams,
        pagination: OffsetPaginationParams,
        status: PositionStatus | None,
        show_with_no_items: bool | None,
        item_status: ItemStatus | None,
    ) -> PositionWithItemsAmountPaginated:
        raise NotImplementedError

    @abstractmethod
    async def read_item(self, item_id: UUID) -> ItemDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def read_items(
        self,
        position_id: PositionId,
        sorting: PositionItemsSortingParams,
        pagination: OffsetPaginationParams,
        status: ItemStatus | None,
    ) -> PositionItemsPaginated:
        raise NotImplementedError
