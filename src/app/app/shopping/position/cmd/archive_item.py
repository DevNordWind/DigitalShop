from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.port import Clock
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import (
    PositionAccessService,
    PositionWarehouseDomainService,
)


@dataclass(slots=True, frozen=True)
class ArchivePositionItemCmd:
    item_id: UUID


class ArchivePositionItem:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
        warehouse_service: PositionWarehouseDomainService,
        clock: Clock,
    ):
        self._repository = repository
        self._session = session
        self._actor_provider = actor_provider
        self._warehouse_service = warehouse_service
        self._clock = clock

    async def __call__(self, cmd: ArchivePositionItemCmd) -> None:
        PositionAccessService.ensure_can_archive(actor=await self._actor_provider.get())

        position: Position | None = await self._repository.get_by_item_id(
            item_id=cmd.item_id
        )

        if not position:
            raise PositionNotFoundError

        await self._warehouse_service.archive(position=position, ids=[cmd.item_id])

        await self._session.commit()
