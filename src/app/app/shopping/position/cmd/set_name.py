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
class SetPositionNameCmd:
    id: UUID
    name: str
    lang: Language


class SetPositionName:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
        clock: Clock,
    ):
        self._repository: PositionRepository = repository
        self._session: DatabaseSession = session
        self._actor_provider: ActorProvider = actor_provider
        self._clock: Clock = clock

    async def __call__(self, cmd: SetPositionNameCmd) -> None:
        PositionAccessService.ensure_can_edit(actor=await self._actor_provider.get())

        position: Position | None = await self._repository.get(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFoundError

        position.set_name(
            lang=cmd.lang,
            name=cmd.name,
            now=self._clock.now(),
        )

        await self._session.commit()
