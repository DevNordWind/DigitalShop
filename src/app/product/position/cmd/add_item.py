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
class AddPositionItemCmd:
    id: UUID
    item_raw: ItemRawDTO


class AddPositionItem:
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

    async def __call__(self, cmd: AddPositionItemCmd) -> ItemId:
        creator: User = await self._current_user()

        position: Position | None = await self._repository.get(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFound

        item: Item = await self._warehouse.add_item(
            creator=creator,
            position=position,
            item_raw=ItemRawMapper.to_value_object(src=cmd.item_raw),
        )
        item_id = item.id

        await self._repository.add_item(item)
        await self._session.commit()

        return item_id
