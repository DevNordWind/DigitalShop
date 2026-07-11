from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.file_key import FileKeyRawDTO, FileKeyRawMapper
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.file_storage import File, FileStorageSession
from app.app.common.port.session import DatabaseSession
from app.domain.common.port import Clock
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.factory import PositionMediaKeyFactory
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import PositionAccessService
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class AddPositionMediaCmd:
    id: UUID
    media: FileKeyRawDTO


class AddPositionMedia:
    def __init__(
        self,
        repository: PositionRepository,
        file_session: FileStorageSession,
        session: DatabaseSession,
        actor_provider: ActorProvider,
        media_key_factory: PositionMediaKeyFactory,
        clock: Clock,
    ):
        self._repository: PositionRepository = repository
        self._file_session: FileStorageSession = file_session
        self._session: DatabaseSession = session
        self._actor_provider: ActorProvider = actor_provider
        self._media_key_factory: PositionMediaKeyFactory = media_key_factory
        self._clock: Clock = clock

    async def __call__(self, cmd: AddPositionMediaCmd) -> None:
        PositionAccessService.ensure_can_edit(actor=await self._actor_provider.get())

        position: Position | None = await self._repository.get(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFoundError

        new_key = self._media_key_factory.generate(
            category_id=position.category_id,
            position_id=position.id,
            raw=FileKeyRawMapper.to_value_object(src=cmd.media),
        )
        position.add_media(media=new_key, now=self._clock.now())

        await self._file_session.put(file=File(key=new_key, content=cmd.media.content))
        await self._file_session.commit()

        await self._session.commit()
