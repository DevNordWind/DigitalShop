from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.file_storage import FileStorageSession
from app.app.common.port.session import DatabaseSession
from app.app.shopping.position.dto.item_content import ItemContentDTO, ItemContentMapper
from app.domain.common.port import Clock
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import (
    PositionAccessService,
    PositionWarehouseDomainService,
)


@dataclass(slots=True, frozen=True)
class ReplacePositionItemCmd:
    item_id: UUID
    new_content: ItemContentDTO


class ReplacePositionItem:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        warehouse_service: PositionWarehouseDomainService,
        file_session: FileStorageSession,
        clock: Clock,
        actor_provider: ActorProvider,
    ):
        self._repository = repository
        self._session = session
        self._warehouse_service = warehouse_service
        self._file_session = file_session
        self._clock = clock
        self._actor_provider = actor_provider

    async def __call__(self, cmd: ReplacePositionItemCmd) -> None:
        PositionAccessService.ensure_can_replace_item(
            actor=await self._actor_provider.get()
        )
        position: Position | None = await self._repository.get_by_item_id(
            item_id=cmd.item_id
        )
        if not position:
            raise PositionNotFoundError

        await self._warehouse_service.replace(
            position=position,
            item_id=cmd.item_id,
            new_content=ItemContentMapper.to_value_object(src=cmd.new_content),
        )

        await self._session.commit()
