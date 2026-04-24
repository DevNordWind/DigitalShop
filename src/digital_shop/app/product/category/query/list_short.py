from dataclasses import dataclass

from app.common.dto.query_params import OffsetPaginationParams
from app.product.category.dto.paginated import CategoriesShortPaginated
from app.product.category.dto.sorting import CategorySortingParams
from app.product.category.port import CategoryReader
from app.user.port import UserIdentifyProvider
from domain.product.category.enums import CategoryStatus
from domain.product.category.service import CategoryAccessService


@dataclass(slots=True, frozen=True)
class ListShortCategoriesQuery:
    pagination: OffsetPaginationParams
    sorting: CategorySortingParams
    show_with_no_items: bool | None
    status: CategoryStatus | None


class ListShortCategories:
    def __init__(self, reader: CategoryReader, idp: UserIdentifyProvider):
        self._reader: CategoryReader = reader
        self._idp: UserIdentifyProvider = idp

    async def __call__(
        self,
        query: ListShortCategoriesQuery,
    ) -> CategoriesShortPaginated:
        resolved_status: CategoryStatus | None = (
            CategoryAccessService.resolve_visible_status(
                viewer_role=await self._idp.get_role(),
                requested_status=query.status,
            )
        )

        return await self._reader.read_short_all(
            pagination=query.pagination,
            sorting=query.sorting,
            status=resolved_status,
            show_with_no_items=query.show_with_no_items,
        )
