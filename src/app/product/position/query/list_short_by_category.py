from dataclasses import dataclass
from uuid import UUID

from app.common.dto.query_params import OffsetPaginationParams
from app.product.position.dto.paginated import PositionsShortPaginated
from app.product.position.dto.sorting import PositionSortingParams
from app.product.position.port import PositionReader
from app.user.port import UserIdentifyProvider
from domain.product.category.value_object import CategoryId
from domain.product.position.enums import PositionStatus
from domain.product.position.service import PositionAccessService


@dataclass(slots=True, frozen=True)
class ListPositionsShortByCategoryQuery:
    category_id: UUID
    pagination: OffsetPaginationParams
    sorting: PositionSortingParams
    show_with_no_items: bool | None
    status: PositionStatus | None


class ListPositionsShortByCategory:
    def __init__(self, reader: PositionReader, idp: UserIdentifyProvider):
        self._reader: PositionReader = reader
        self._idp: UserIdentifyProvider = idp

    async def __call__(
        self,
        query: ListPositionsShortByCategoryQuery,
    ) -> PositionsShortPaginated:
        resolved_status: PositionStatus | None = (
            PositionAccessService.resolve_visible_status(
                viewer_role=await self._idp.get_role(),
                requested_status=query.status,
            )
        )

        return await self._reader.read_short_by_category_id(
            category_id=CategoryId(query.category_id),
            pagination=query.pagination,
            sorting=query.sorting,
            show_with_no_items=query.show_with_no_items,
            status=resolved_status,
        )
