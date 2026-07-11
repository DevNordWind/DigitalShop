from dataclasses import dataclass

from app.app.common.dto.query_params import OffsetPaginationParams
from app.app.common.port.actor_provider import ActorProvider
from app.app.shopping.category.dto.paginated import CategoriesPaginated
from app.app.shopping.category.dto.sorting import CategorySortingParams
from app.app.shopping.category.port import CategoryReader
from app.domain.shopping.category.enums import CategoryStatus
from app.domain.shopping.category.service import CategoryAccessService


@dataclass(slots=True, frozen=True)
class ListCategoriesQuery:
    pagination: OffsetPaginationParams
    sorting: CategorySortingParams
    status: CategoryStatus | None


class ListCategories:
    def __init__(self, reader: CategoryReader, actor_provider: ActorProvider):
        self._reader = reader
        self._actor_provider = actor_provider

    async def __call__(
        self,
        query: ListCategoriesQuery,
    ) -> CategoriesPaginated:
        resolved_status: CategoryStatus | None = (
            CategoryAccessService.resolve_visible_status(
                actor=await self._actor_provider.get(),
                requested_status=query.status,
            )
        )

        return await self._reader.read_all(
            pagination=query.pagination,
            sorting=query.sorting,
            status=resolved_status,
        )
