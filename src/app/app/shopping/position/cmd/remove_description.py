from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.localized import Language
from app.domain.common.port import Clock
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import PositionAccessService
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class RemovePositionDescriptionCmd:
    id: UUID
    lang: Language


class RemovePositionDescription:
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

    async def __call__(self, cmd: RemovePositionDescriptionCmd) -> None:
        PositionAccessService.ensure_can_edit(actor=await self._actor_provider.get())
        position: Position | None = await self._repository.get(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFoundError

        position.remove_description(lang=cmd.lang, now=self._clock.now())

        await self._session.commit()
