from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.item.enums import GenericItemStatus
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import (
    PositionAccessService,
    PositionWarehouseDomainService,
)
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class DeleteAllPositionItemsCmd:
    position_id: UUID


class DeleteAllPositionItems:
    def __init__(
        self,
        repo: PositionRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
        warehouse_service: PositionWarehouseDomainService,
    ):
        self._repo = repo
        self._session = session
        self._actor_provider = actor_provider
        self._warehouse_service = warehouse_service

    async def __call__(self, cmd: DeleteAllPositionItemsCmd) -> None:
        PositionAccessService.ensure_can_delete_item(
            actor=await self._actor_provider.get()
        )

        position, ids = await self._repo.get_with_items_ids(
            position_id=PositionId(cmd.position_id),
            item_status=GenericItemStatus.ARCHIVED,
        )
        if not position:
            raise PositionNotFoundError

        await self._warehouse_service.delete(position=position, ids=ids)
        await self._session.commit()
