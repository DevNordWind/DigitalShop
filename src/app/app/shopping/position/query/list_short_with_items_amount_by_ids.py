from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.query_params import OffsetPaginationParams
from app.app.common.port.actor_provider import ActorProvider
from app.app.shopping.position.dto.item import ItemStatus
from app.app.shopping.position.dto.paginated import (
    PositionShortWithItemsAmountPaginated,
)
from app.app.shopping.position.dto.sorting import PositionSortingParams
from app.app.shopping.position.port import PositionReader
from app.domain.common.actor import Actor
from app.domain.shopping.position.service import PositionAccessService
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class ListPositionsShortWithItemsAmountByIdsQuery:
    ids: list[UUID]
    pagination: OffsetPaginationParams
    sorting: PositionSortingParams

    show_with_no_items: bool | None
    status: ItemStatus | None


class ListPositionsShortWithItemsAmountByIds:
    def __init__(self, reader: PositionReader, actor_provider: ActorProvider):
        self._reader = reader
        self._actor_provider = actor_provider

    async def __call__(
        self,
        query: ListPositionsShortWithItemsAmountByIdsQuery,
    ) -> PositionShortWithItemsAmountPaginated:
        paginated: PositionShortWithItemsAmountPaginated = (
            await self._reader.read_short_with_items_amount_by_ids(
                position_ids=[PositionId(id_) for id_ in query.ids],
                pagination=query.pagination,
                sorting=query.sorting,
                item_status=query.status,
            )
        )
        actor: Actor = await self._actor_provider.get()

        for page in paginated.positions:
            PositionAccessService.ensure_can_view(
                actor=actor, position_status=page.position.status
            )

        return paginated
