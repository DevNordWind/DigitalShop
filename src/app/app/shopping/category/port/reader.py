from abc import ABC, abstractmethod

from app.app.common.dto.query_params import OffsetPaginationParams
from app.app.shopping.category.dto.category import (
    CategoryDTO,
    CategoryShortDTO,
    CategoryWithGoodsAmountDTO,
)
from app.app.shopping.category.dto.paginated import (
    CategoriesPaginated,
    CategoriesShortPaginated,
)
from app.app.shopping.category.dto.sorting import CategorySortingParams
from app.domain.shopping.category.enums import CategoryStatus
from app.domain.shopping.category.value_object import CategoryId


class CategoryReader(ABC):
    @abstractmethod
    async def read(self, category_id: CategoryId) -> CategoryDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def read_short(
        self,
        category_id: CategoryId,
    ) -> CategoryShortDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def read_with_goods_amount(
        self,
        category_id: CategoryId,
    ) -> CategoryWithGoodsAmountDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def read_all(
        self,
        pagination: OffsetPaginationParams,
        sorting: CategorySortingParams,
        status: CategoryStatus | None,
    ) -> CategoriesPaginated:
        raise NotImplementedError

    @abstractmethod
    async def read_short_all(
        self,
        pagination: OffsetPaginationParams,
        sorting: CategorySortingParams,
        show_with_no_items: bool | None,
        status: CategoryStatus | None,
    ) -> CategoriesShortPaginated:
        raise NotImplementedError
