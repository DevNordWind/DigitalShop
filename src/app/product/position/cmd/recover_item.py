from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.product.position.exception import (
    PositionItemNotFound,
    PositionNotFound,
)
from app.user.port import UserIdentifyProvider
from domain.common.port import Clock
from domain.product.position.entity import Position
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.item.entity import Item
from domain.product.position.item.value_object import ItemId
from domain.product.position.port import PositionRepository
from domain.product.position.service import (
    PositionAccessService,
    PositionWarehouseService,
)


@dataclass(slots=True, frozen=True)
class RecoverPositionItemCmd:
    item_id: UUID


class RecoverPositionItem:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        warehouse_service: PositionWarehouseService,
        idp: UserIdentifyProvider,
        clock: Clock,
    ):
        self._repository: PositionRepository = repository
        self._session: DatabaseSession = session
        self._warehouse_service: PositionWarehouseService = warehouse_service
        self._idp: UserIdentifyProvider = idp
        self._clock: Clock = clock

    async def __call__(self, cmd: RecoverPositionItemCmd) -> None:
        if not PositionAccessService.can_recover(
            recoverer_role=await self._idp.get_role(),
        ):
            raise PositionPermissionDenied

        item: Item | None = await self._repository.get_item_for_update(
            item_id=ItemId(cmd.item_id),
        )
        if not item:
            raise PositionItemNotFound

        position: Position | None = await self._repository.get_for_update(
            position_id=item.position_id,
        )
        if not position:
            raise PositionNotFound

        await self._warehouse_service.recover_item(position, item)
        await self._session.commit()
