from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.file_key import FileKeyDTO
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.file_storage import FileStorageSession
from app.app.common.port.session import DatabaseSession
from app.app.shopping.position.dto.media_key import PositionMediaKeyMapper
from app.domain.common.port import Clock
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import PositionAccessService
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class RemovePositionMediaCmd:
    id: UUID
    media: FileKeyDTO


class RemovePositionMedia:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
        file_serssion: FileStorageSession,
        clock: Clock,
    ):
        self._repository = repository
        self._session = session
        self._actor_provider = actor_provider
        self._file_session = file_serssion
        self._clock = clock

    async def __call__(self, cmd: RemovePositionMediaCmd) -> None:
        PositionAccessService.ensure_can_edit(actor=await self._actor_provider.get())

        position: Position | None = await self._repository.get(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFoundError

        key = PositionMediaKeyMapper.to_value_object(src=cmd.media)
        position.remove_media(media=key, now=self._clock.now())
        await self._file_session.delete(key=key)

        await self._session.commit()
        await self._file_session.commit()
