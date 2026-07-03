from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.shopping.position.dto.item import ItemStatus
from app.app.shopping.position.dto.position import PositionWithItemsAmount
from app.app.shopping.position.port import PositionReader
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.service import PositionAccessService
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class GetPositionWithItemsAmountQuery:
    id: UUID
    item_status: ItemStatus | None


class GetPositionWithItemsAmount:
    def __init__(self, reader: PositionReader, actor_provider: ActorProvider):
        self._reader = reader
        self._actor_provider = actor_provider

    async def __call__(
        self,
        query: GetPositionWithItemsAmountQuery,
    ) -> PositionWithItemsAmount:
        dto: PositionWithItemsAmount | None = await self._reader.read_with_items_amount(
            position_id=PositionId(query.id), item_status=query.item_status
        )
        if dto is None:
            raise PositionNotFoundError

        PositionAccessService.ensure_can_view(
            actor=await self._actor_provider.get(), position_status=dto.position.status
        )

        return dto
