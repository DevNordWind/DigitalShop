from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.file_storage import FileStorageSession
from app.app.common.port.session import DatabaseSession
from app.domain.shopping.category.value_object import CategoryId
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.enums import PositionStatus
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import (
    PositionAccessService,
)


@dataclass(slots=True, frozen=True)
class DeleteAllPositionsByCategoryCmd:
    category_id: UUID


class DeleteAllPositionsByCategory:
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

    async def __call__(self, cmd: DeleteAllPositionsByCategoryCmd) -> None:
        PositionAccessService.ensure_can_delete(actor=await self._actor_provider.get())

        positions: list[Position] = await self._repo.acquire_by_category_ids_status(
            category_ids=[CategoryId(cmd.category_id)], status=PositionStatus.ARCHIVED
        )
        for position in positions:
            position.ensure_deletable()
            for key in position.media:
                await self._file_session.delete(key=key)

            await self._repo.delete(position)

        await self._session.commit()
        await self._file_session.commit()
