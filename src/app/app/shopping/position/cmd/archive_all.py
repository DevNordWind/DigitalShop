from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.port import Clock
from app.domain.shopping.category.value_object import CategoryId
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.enums import PositionStatus
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import PositionAccessService


@dataclass(slots=True, frozen=True)
class ArchiveAllPositionsByCategoryCmd:
    category_id: UUID


class ArchiveAllPositionsByCategory:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
        clock: Clock,
    ):
        self._repository = repository
        self._session = session
        self._actor_provider = actor_provider
        self._clock = clock

    async def __call__(self, cmd: ArchiveAllPositionsByCategoryCmd) -> None:
        PositionAccessService.ensure_can_archive(actor=await self._actor_provider.get())

        positions: list[
            Position
        ] = await self._repository.acquire_by_category_ids_status(
            category_ids=[CategoryId(cmd.category_id)], status=PositionStatus.AVAILABLE
        )
        if not positions:
            raise PositionNotFoundError

        now: datetime = self._clock.now()

        for position in positions:
            position.archive(now)

        await self._session.commit()
