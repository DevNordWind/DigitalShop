from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession, FileStorageSession
from app.product.position.exception import PositionNotFound
from app.user.port import UserIdentifyProvider
from domain.product.position.entity import Position
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionAccessService
from domain.product.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class DeletePositionCmd:
    id: UUID


class DeletePosition:
    def __init__(
        self,
        repo: PositionRepository,
        session: DatabaseSession,
        file_session: FileStorageSession,
        idp: UserIdentifyProvider,
    ):
        self._repo: PositionRepository = repo
        self._session: DatabaseSession = session
        self._file_session: FileStorageSession = file_session
        self._idp: UserIdentifyProvider = idp

    async def __call__(self, cmd: DeletePositionCmd) -> None:
        if not PositionAccessService.can_delete(
            deleter_role=await self._idp.get_role(),
        ):
            raise PositionPermissionDenied

        position: Position | None = await self._repo.get_for_update(
            position_id=PositionId(cmd.id),
        )
        if not position:
            raise PositionNotFound

        position.ensure_deletable()

        for media in position.media:
            await self._file_session.delete(media)

        await self._repo.delete(position)
        await self._session.commit()
        if position.media:
            await self._file_session.commit()
