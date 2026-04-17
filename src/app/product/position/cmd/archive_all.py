from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.common.port import DatabaseSession
from app.user.service import GetCurrentUser
from domain.common.port import Clock
from domain.product.category.value_object import CategoryId
from domain.product.position.entity import Position
from domain.product.position.enums import PositionStatus
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionAccessService
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class ArchiveAllPositionsInCategoryCmd:
    category_id: UUID


class ArchiveAllPositionsInCategory:
    def __init__(
        self,
        repository: PositionRepository,
        session: DatabaseSession,
        current_user: GetCurrentUser,
        clock: Clock,
    ):
        self._repository: PositionRepository = repository
        self._session: DatabaseSession = session
        self._current_user: GetCurrentUser = current_user
        self._clock: Clock = clock

    async def __call__(self, cmd: ArchiveAllPositionsInCategoryCmd) -> None:
        archiver: User = await self._current_user()

        if not PositionAccessService.can_archive(archiver_role=archiver.role):
            raise PositionPermissionDenied

        positions: list[
            Position
        ] = await self._repository.get_by_category_ids_for_update(
            category_ids=[CategoryId(cmd.category_id)],
            status=PositionStatus.AVAILABLE,
        )
        if not positions:
            return

        now: datetime = self._clock.now()

        for position in positions:
            position.archive(now)

        await self._session.commit()
