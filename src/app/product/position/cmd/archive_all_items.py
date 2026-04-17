from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.common.port import DatabaseSession
from app.user.service import GetCurrentUser
from domain.common.port import Clock
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.item.entity import Item
from domain.product.position.item.enums import ItemStatus
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionAccessService
from domain.product.position.value_object import PositionId
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class ArchiveAllPositionItemsCmd:
    position_id: UUID


class ArchiveAllPositionItems:
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

    async def __call__(self, cmd: ArchiveAllPositionItemsCmd) -> None:
        archiver: User = await self._current_user()
        if not PositionAccessService.can_archive_item(
            archiver_role=archiver.role,
        ):
            raise PositionPermissionDenied

        items: list[Item] = await self._repository.get_items_for_update(
            position_id=PositionId(cmd.position_id),
            status=ItemStatus.AVAILABLE,
        )
        if not items:
            return

        now: datetime = self._clock.now()
        for item in items:
            item.archive(now=now)

        await self._session.commit()
