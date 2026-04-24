from dataclasses import dataclass
from uuid import UUID

from app.common.dto.file_key import (
    FileKeyDTO,
    FileKeyRawDTO,
    FileKeyRawMapper,
)
from app.common.port import DatabaseSession, FileStorageSession
from app.product.position.dto.media_key import PositionMediaKeyMapper
from app.product.position.exception import PositionNotFound
from app.user.service import GetCurrentUser
from domain.common.port import Clock
from domain.product.position.entity import Position
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.port import PositionRepository
from domain.product.position.service import (
    PositionAccessService,
    PositionMediaKeyFactory,
)
from domain.product.position.value_object import PositionId, PositionMediaKey
from domain.user.entity import User


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
        current_user: GetCurrentUser,
        file_session: FileStorageSession,
        media_key_factory: PositionMediaKeyFactory,
        clock: Clock,
    ):
        self._repository: PositionRepository = repository
        self._session: DatabaseSession = session
        self._current_user: GetCurrentUser = current_user
        self._file_session: FileStorageSession = file_session
        self._media_key_factory: PositionMediaKeyFactory = media_key_factory
        self._clock: Clock = clock

    async def __call__(self, cmd: ReplacePositionMediaCmd) -> None:
        editor: User = await self._current_user()

        if not PositionAccessService.can_edit(editor_role=editor.role):
            raise PositionPermissionDenied

        position: Position | None = await self._repository.get(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFound

        old_key: PositionMediaKey = PositionMediaKeyMapper.to_value_object(
            src=cmd.old_media,
        )

        new_key: PositionMediaKey = self._media_key_factory.generate(
            category_id=position.category_id,
            position_id=position.id,
            raw=FileKeyRawMapper.to_value_object(cmd.new_media),
        )

        position.replace_media(old=old_key, new=new_key, now=self._clock.now())

        await self._file_session.delete(old_key)
        await self._file_session.put(new_key, cmd.new_media.content)
        await self._file_session.commit()

        await self._session.commit()
