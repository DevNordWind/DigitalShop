from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.query_params import OffsetPaginationParams
from app.app.common.port.actor_provider import ActorProvider
from app.app.shopping.position.dto.item import ItemStatus
from app.app.shopping.position.dto.paginated import PositionItemsPaginated
from app.app.shopping.position.dto.sorting import PositionItemsSortingParams
from app.app.shopping.position.port import PositionReader
from app.domain.shopping.position.service import PositionAccessService
from app.domain.shopping.position.value_object import PositionId


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
        actor_provider: ActorProvider,
    ):
        self._reader: PositionReader = reader
        self._actor_provider: ActorProvider = actor_provider

    async def __call__(
        self,
        query: ListPositionItemsQuery,
    ) -> PositionItemsPaginated:
        PositionAccessService.ensure_can_view_item(
            actor=await self._actor_provider.get()
        )

        return await self._reader.read_items(
            position_id=PositionId(query.id),
            sorting=query.sorting,
            pagination=query.pagination,
            status=query.status,
        )
