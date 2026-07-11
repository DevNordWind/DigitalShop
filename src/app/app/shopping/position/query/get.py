from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.shopping.position.dto.position import PositionDTO
from app.app.shopping.position.port import PositionReader
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.service import PositionAccessService
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class GetPositionQuery:
    id: UUID


class GetPosition:
    def __init__(self, reader: PositionReader, actor_provider: ActorProvider):
        self._reader = reader
        self._actor_provider = actor_provider

    async def __call__(self, query: GetPositionQuery) -> PositionDTO:
        position: PositionDTO | None = await self._reader.read(
            position_id=PositionId(query.id),
        )
        if not position:
            raise PositionNotFoundError

        PositionAccessService.ensure_can_view(
            actor=await self._actor_provider.get(), position_status=position.status
        )

        return position
