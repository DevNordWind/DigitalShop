from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.query_params import OffsetPaginationParams
from app.app.common.port.actor_provider import ActorProvider
from app.app.shopping.position.dto.paginated import PositionsShortPaginated
from app.app.shopping.position.dto.sorting import PositionSortingParams
from app.app.shopping.position.port import PositionReader
from app.domain.shopping.category.value_object import CategoryId
from app.domain.shopping.position.enums import PositionStatus
from app.domain.shopping.position.service import PositionAccessService


@dataclass(slots=True, frozen=True)
class ListPositionsShortByCategoryQuery:
    category_id: UUID
    pagination: OffsetPaginationParams
    sorting: PositionSortingParams
    show_with_no_items: bool | None
    status: PositionStatus | None


class ListPositionsShortByCategory:
    def __init__(self, reader: PositionReader, actor_provider: ActorProvider):
        self._reader = reader
        self._actor_provider = actor_provider

    async def __call__(
        self,
        query: ListPositionsShortByCategoryQuery,
    ) -> PositionsShortPaginated:

        resolved_status: PositionStatus | None = (
            PositionAccessService.resolve_visible_status(
                requested_status=query.status, actor=await self._actor_provider.get()
            )
        )

        return await self._reader.read_short_by_category_id(
            category_id=CategoryId(query.category_id),
            pagination=query.pagination,
            sorting=query.sorting,
            show_with_no_items=query.show_with_no_items,
            status=resolved_status,
        )
