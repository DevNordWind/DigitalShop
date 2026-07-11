from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.file_storage import FileStorageSession
from app.app.common.port.session import DatabaseSession
from app.domain.shopping.position.exception import PositionNotFoundError
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import (
    PositionAccessService,
)
from app.domain.shopping.position.value_object import PositionId


@dataclass(slots=True, frozen=True)
class DeletePositionCmd:
    id: UUID


class DeletePosition:
    def __init__(
        self,
        repo: PositionRepository,
        session: DatabaseSession,
        file_session: FileStorageSession,
        actor_provider: ActorProvider,
    ):
        self._repo = repo
        self._session = session
        self._file_session = file_session
        self._actor_provider = actor_provider

    async def __call__(self, cmd: DeletePositionCmd) -> None:
        PositionAccessService.ensure_can_delete(actor=await self._actor_provider.get())

        position = await self._repo.get(position_id=PositionId(cmd.id))
        if not position:
            raise PositionNotFoundError

        position.ensure_deletable()
        for key in position.media:
            await self._file_session.delete(key=key)

        await self._repo.delete(position)

        await self._session.commit()
        await self._file_session.commit()
