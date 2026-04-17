from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.product.position.dto.item_content import (
    ItemRawDTO,
    ItemRawMapper,
)
from app.product.position.exception import PositionNotFound
from app.user.service import GetCurrentUser
from domain.common.port import Clock
from domain.product.position.entity import Position
from domain.product.position.item.entity import Item
from domain.product.position.item.value_object import (
    ItemId,
)
from domain.product.position.port import PositionRepository
from domain.product.position.service import (
    PositionWarehouseService,
)
from domain.product.position.value_object import PositionId
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class AddPositionItemsCmd:
    id: UUID
    items_raw: list[ItemRawDTO]


class AddPositionItems:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        warehouse: PositionWarehouseService,
        current_user: GetCurrentUser,
        clock: Clock,
    ):
        self._repository: PositionRepository = repository
        self._session: DatabaseSession = session
        self._warehouse: PositionWarehouseService = warehouse
        self._current_user: GetCurrentUser = current_user
        self._clock: Clock = clock

    async def __call__(self, cmd: AddPositionItemsCmd) -> list[ItemId]:
        creator: User = await self._current_user()

        position: Position | None = await self._repository.get(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFound

        items_raw = [
            ItemRawMapper.to_value_object(src=item_raw)
            for item_raw in cmd.items_raw
        ]

        items: list[Item] = await self._warehouse.add_items(
            creator=creator,
            position=position,
            items_raw=items_raw,
        )
        items_ids: list[ItemId] = [item.id for item in items]

        await self._repository.add_items(items)
        await self._session.commit()

        return items_ids
