from abc import ABC, abstractmethod

from app.common.dto.query_params import OffsetPaginationParams
from app.product.position.dto.item import ItemDTO
from app.product.position.dto.paginated import (
    PositionItemsPaginated,
    PositionsPaginated,
    PositionsShortPaginated,
    PositionWithItemsAmountPaginated,
)
from app.product.position.dto.position import (
    PositionDTO,
    PositionShortDTO,
    PositionWithItemsAmount,
)
from app.product.position.dto.sorting import (
    PositionItemsSortingParams,
    PositionSortingParams,
)
from domain.product.category.value_object import CategoryId
from domain.product.position.enums import PositionStatus
from domain.product.position.item.enums import ItemStatus
from domain.product.position.item.value_object import ItemId
from domain.product.position.value_object import PositionId


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
        self,
        position_id: PositionId,
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
    ) -> PositionWithItemsAmountPaginated:
        raise NotImplementedError

    @abstractmethod
    async def read_item(self, item_id: ItemId) -> ItemDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def read_position_items_by_warehouse(
        self,
        position_id: PositionId,
        sorting: PositionItemsSortingParams,
        pagination: OffsetPaginationParams,
        status: ItemStatus | None,
    ) -> PositionItemsPaginated:
        raise NotImplementedError
