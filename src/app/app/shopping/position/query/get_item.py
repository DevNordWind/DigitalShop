from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.shopping.position.dto.item import ItemDTO
from app.app.shopping.position.port import PositionReader
from app.domain.shopping.position.exception import PositionItemNotFoundError
from app.domain.shopping.position.service import PositionAccessService


@dataclass(slots=True, frozen=True)
class GetPositionItemQuery:
    item_id: UUID


class GetPositionItem:
    def __init__(
        self,
        reader: PositionReader,
        actor_provider: ActorProvider,
    ):
        self._reader: PositionReader = reader
        self._actor_provider: ActorProvider = actor_provider

    async def __call__(self, query: GetPositionItemQuery) -> ItemDTO:
        PositionAccessService.ensure_can_view_item(
            actor=await self._actor_provider.get()
        )

        item: ItemDTO | None = await self._reader.read_item(
            item_id=query.item_id,
        )
        if not item:
            raise PositionItemNotFoundError

        return item
