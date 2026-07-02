from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.app.shopping.position.dto.item_content import (
    ItemContentDTO,
    ItemContentMapper,
)
from app.domain.common.actor import UserActor
from app.domain.common.port import Clock
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.item.value_object import ItemSnapshot
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import (
    PositionAccessService,
    PositionWarehouseDomainService,
)
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class AddPositionItemsCmd:
    id: UUID
    contents: list[ItemContentDTO]


class AddPositionItems:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        warehouse: PositionWarehouseDomainService,
        actor_provider: ActorProvider,
        clock: Clock,
    ):
        self._repository = repository
        self._session = session
        self._warehouse = warehouse
        self._actor_provider = actor_provider
        self._clock = clock

    async def __call__(self, cmd: AddPositionItemsCmd) -> list[UUID]:
        actor: UserActor = PositionAccessService.ensure_can_add_item(
            actor=await self._actor_provider.get()
        )
        position: Position | None = await self._repository.get(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFoundError

        snapshots: tuple[ItemSnapshot, ...] = await self._warehouse.add(
            creator_id=actor.id,
            position=position,
            contents=[
                ItemContentMapper.to_value_object(src=content)
                for content in cmd.contents
            ],
        )

        await self._session.commit()

        return [item.id for item in snapshots]
