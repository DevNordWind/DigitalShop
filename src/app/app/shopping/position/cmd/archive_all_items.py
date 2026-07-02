from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.port import Clock
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.item.enums import GenericItemStatus
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import (
    PositionAccessService,
    PositionWarehouseDomainService,
)
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class ArchiveAllPositionItemsCmd:
    position_id: UUID


class ArchiveAllPositionItems:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        warehouse_service: PositionWarehouseDomainService,
        actor_provider: ActorProvider,
        clock: Clock,
    ):
        self._repository = repository
        self._session = session
        self._warehouse_service = warehouse_service
        self._actor_provider = actor_provider
        self._clock = clock

    async def __call__(self, cmd: ArchiveAllPositionItemsCmd) -> None:
        PositionAccessService.ensure_can_archive_item(
            actor=await self._actor_provider.get()
        )

        position, items_ids = await self._repository.get_with_items_ids(
            position_id=PositionId(cmd.position_id),
            item_status=GenericItemStatus.AVAILABLE,
        )
        if position is None:
            raise PositionNotFoundError

        await self._warehouse_service.archive(position=position, ids=items_ids)

        await self._session.commit()
