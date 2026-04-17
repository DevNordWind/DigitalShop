from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.product.position.exception import (
    PositionItemNotFound,
)
from app.user.service import GetCurrentUser
from domain.common.port import Clock
from domain.product.position.exception import PositionPermissionDenied
from domain.product.position.item.entity import Item
from domain.product.position.item.value_object import ItemId
from domain.product.position.port import PositionRepository
from domain.product.position.service import PositionAccessService
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class ArchivePositionItemCmd:
    item_id: UUID


class ArchivePositionItem:
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

    async def __call__(self, cmd: ArchivePositionItemCmd) -> None:
        archiver: User = await self._current_user()
        if not PositionAccessService.can_archive_item(
            archiver_role=archiver.role,
        ):
            raise PositionPermissionDenied

        item: Item | None = await self._repository.get_item_for_update(
            item_id=ItemId(cmd.item_id),
        )
        if not item:
            raise PositionItemNotFound

        item.archive(now=self._clock.now())

        await self._session.commit()
