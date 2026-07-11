from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import (
    PositionAccessService,
    PositionWarehouseDomainService,
)


@dataclass(slots=True, frozen=True)
class DeletePositionItemCmd:
    item_id: UUID


class DeletePositionItem:
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

    async def __call__(self, cmd: DeletePositionItemCmd) -> None:
        PositionAccessService.ensure_can_delete_item(
            actor=await self._actor_provider.get()
        )

        position: Position | None = await self._repo.get_by_item_id(item_id=cmd.item_id)
        if not position:
            raise PositionNotFoundError

        await self._warehouse_service.delete(position=position, ids=[cmd.item_id])
        await self._session.commit()
