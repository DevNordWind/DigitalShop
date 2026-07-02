from dataclasses import dataclass
from datetime import datetime

from app.domain.shopping.position.item.enums import (
    FixedItemStatus,
)
from app.domain.shopping.position.item.exception import (
    FixedItemArchivationForbiddenError,
    FixedItemContentReplacingForbiddenError,
    FixedItemDeletionForbiddenError,
    FixedItemRecoverForbiddenError,
)
from app.domain.shopping.position.item.value_object import (
    FixedItemId,
    ItemContent,
    ItemSnapshot,
)
from app.domain.shopping.position.value_object import PositionId
from app.domain.user.value_object import UserId


@dataclass
class FixedItem:
    id: FixedItemId
    position_id: PositionId
    creator_id: UserId

    content: ItemContent
    status: FixedItemStatus

    created_at: datetime

    archived_at: datetime | None = None
    updated_at: datetime | None = None

    def take_snapshot(self) -> ItemSnapshot:
        return ItemSnapshot(id=self.id.value, content=self.content)

    def archive(self, now: datetime) -> None:
        if self.status != FixedItemStatus.AVAILABLE:
            raise FixedItemArchivationForbiddenError

        self.archived_at = now
        self.status = FixedItemStatus.ARCHIVED

    def recover(self) -> None:
        if self.status != FixedItemStatus.ARCHIVED:
            raise FixedItemRecoverForbiddenError

        self.status = FixedItemStatus.AVAILABLE
        self.archived_at = None

    def replace_content(
        self,
        new_content: ItemContent,
        now: datetime,
    ) -> None:
        if self.status != FixedItemStatus.AVAILABLE:
            raise FixedItemContentReplacingForbiddenError

        if new_content == self.content:
            return None

        self.content = new_content
        self.updated_at = now

    def ensure_can_delete(self) -> None:
        if self.status != FixedItemStatus.ARCHIVED:
            raise FixedItemDeletionForbiddenError
