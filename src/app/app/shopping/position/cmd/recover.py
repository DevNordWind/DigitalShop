from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.port import Clock
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import (
    PositionAccessService,
)
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class RecoverPositionCmd:
    id: UUID


class RecoverPosition:
    def __init__(
        self,
        repo: PositionRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
        clock: Clock,
    ):
        self._repo = repo
        self._session = session
        self._actor_provider = actor_provider
        self._clock = clock

    async def __call__(self, cmd: RecoverPositionCmd) -> None:
        PositionAccessService.ensure_can_delete(actor=await self._actor_provider.get())

        position = await self._repo.get(position_id=PositionId(cmd.id))
        if not position:
            raise PositionNotFoundError

        position.recover(now=self._clock.now())

        await self._session.commit()
