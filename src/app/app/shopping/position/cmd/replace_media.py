from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.file_key import FileKeyDTO, FileKeyRawDTO, FileKeyRawMapper
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.file_storage import File, FileStorageSession
from app.app.common.port.session import DatabaseSession
from app.app.shopping.position.dto.media_key import PositionMediaKeyMapper
from app.domain.common.port import Clock
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.factory import PositionMediaKeyFactory
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import PositionAccessService
from app.domain.shopping.position.value_object import PositionId, PositionMediaKey


@dataclass(slots=True, frozen=True)
class ReplacePositionMediaCmd:
    id: UUID
    old_media: FileKeyDTO
    new_media: FileKeyRawDTO


class ReplacePositionMedia:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        actor_provider: ActorProvider,
        file_session: FileStorageSession,
        media_key_factory: PositionMediaKeyFactory,
        clock: Clock,
    ):
        self._repository = repository
        self._session = session
        self._actor_provider = actor_provider
        self._file_session = file_session
        self._media_key_factory = media_key_factory
        self._clock = clock

    async def __call__(self, cmd: ReplacePositionMediaCmd) -> None:
        PositionAccessService.ensure_can_edit(actor=await self._actor_provider.get())
        position: Position | None = await self._repository.get(
            position_id=PositionId(cmd.id)
        )
        if not position:
            raise PositionNotFoundError

        old_key: PositionMediaKey = PositionMediaKeyMapper.to_value_object(
            src=cmd.old_media
        )
        new_key: PositionMediaKey = self._media_key_factory.generate(
            category_id=position.category_id,
            position_id=position.id,
            raw=FileKeyRawMapper.to_value_object(src=cmd.new_media),
        )

        position.replace_media(old=old_key, new=new_key, now=self._clock.now())

        await self._file_session.delete(old_key)
        await self._file_session.put(
            file=File(key=new_key, content=cmd.new_media.content)
        )

        await self._session.commit()
        await self._file_session.commit()
