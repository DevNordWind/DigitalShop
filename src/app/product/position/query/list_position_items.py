from dataclasses import dataclass
from uuid import UUID

from app.common.dto.query_params import OffsetPaginationParams
from app.product.position.dto.paginated import PositionItemsPaginated
from app.product.position.dto.sorting import PositionItemsSortingParams
from app.product.position.port import PositionReader
from app.user.port import UserIdentifyProvider
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.item.enums import (
    ItemStatus,
)
from domain.product.position.service import PositionAccessService
from domain.product.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class ListPositionItemsQuery:
    id: UUID
    sorting: PositionItemsSortingParams
    pagination: OffsetPaginationParams
    status: ItemStatus | None


class ListPositionItems:
    def __init__(
        self,
        reader: PositionReader,
        idp: UserIdentifyProvider,
    ):
        self._reader: PositionReader = reader
        self._idp: UserIdentifyProvider = idp

    async def __call__(
        self,
        query: ListPositionItemsQuery,
    ) -> PositionItemsPaginated:
        if not PositionAccessService.can_view_item(
            viewer_role=await self._idp.get_role(),
        ):
            raise PositionPermissionDenied

        return await self._reader.read_position_items_by_warehouse(
            position_id=PositionId(query.id),
            sorting=query.sorting,
            pagination=query.pagination,
            status=query.status,
        )
