from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession, FileStorageSession
from app.user.port import UserIdentifyProvider
from domain.product.category.value_object import CategoryId
from domain.product.position.entity import Position
from domain.product.position.enums import PositionStatus
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionAccessService


@dataclass(slots=True, frozen=True)
class DeleteAllPositionsInCategoryCmd:
    category_id: UUID


class DeleteAllPositionsInCategory:
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

    async def __call__(self, cmd: DeleteAllPositionsInCategoryCmd) -> None:
        if not PositionAccessService.can_delete(
            deleter_role=await self._idp.get_role(),
        ):
            raise PositionPermissionDenied

        category_id = CategoryId(cmd.category_id)

        positions: list[
            Position
        ] = await self._repo.get_by_category_ids_for_update(
            category_ids=[category_id],
            status=PositionStatus.ARCHIVED,
        )
        for position in positions:
            position.ensure_deletable()
            for media_key in position.media:
                await self._file_session.delete(media_key)

            await self._repo.delete(position)

        await self._session.commit()
        await self._file_session.commit()
