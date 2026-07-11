from dataclasses import dataclass
from datetime import datetime

from app.domain.shopping.position.item.enums import (
    StockItemStatus,
)
from app.domain.shopping.position.item.exception import (
    StockItemArchivationForbiddenError,
    StockItemContentReplacingForbiddenError,
    StockItemDeletionForbiddenError,
    StockItemRecoverForbiddenError,
    StockItemReleaseForbiddenError,
    StockItemReservationForbiddenError,
    StockItemSellForbiddenError,
)
from app.domain.shopping.position.item.value_object import (
    ItemContent,
    ItemSnapshot,
    StockItemId,
)
from app.domain.shopping.position.value_object import PositionId
from app.domain.user.value_object import UserId


@dataclass
class StockItem:
    id: StockItemId
    position_id: PositionId
    creator_id: UserId

    content: ItemContent
    status: StockItemStatus

    created_at: datetime

    archived_at: datetime | None = None
    sold_at: datetime | None = None
    reserved_at: datetime | None = None
    updated_at: datetime | None = None

    def take_snapshot(self) -> ItemSnapshot:
        return ItemSnapshot(id=self.id.value, content=self.content)

    def archive(self, now: datetime) -> None:
        if self.status != StockItemStatus.AVAILABLE:
            raise StockItemArchivationForbiddenError

        self.archived_at = now
        self.status = StockItemStatus.ARCHIVED

    def recover(self) -> None:
        if self.status != StockItemStatus.ARCHIVED:
            raise StockItemRecoverForbiddenError

        self.status = StockItemStatus.AVAILABLE
        self.archived_at = None

    def replace_content(
        self,
        new_content: ItemContent,
        now: datetime,
    ) -> ItemContent | None:
        if self.status != StockItemStatus.AVAILABLE:
            raise StockItemContentReplacingForbiddenError

        if new_content == self.content:
            return None

        old_content = self.content

        self.content = new_content
        self.updated_at = now

        return old_content

    def reserve(self, now: datetime) -> None:
        if self.status != StockItemStatus.AVAILABLE:
            raise StockItemReservationForbiddenError

        self.status = StockItemStatus.RESERVED
        self.reserved_at = now

    def release(self) -> None:
        if self.status != StockItemStatus.RESERVED:
            raise StockItemReleaseForbiddenError

        self.status = StockItemStatus.AVAILABLE
        self.reserved_at = None

    def sell(self, now: datetime) -> None:
        if self.status != StockItemStatus.RESERVED:
            raise StockItemSellForbiddenError

        self.sold_at = now
        self.status = StockItemStatus.SOLD

    def ensure_can_delete(self) -> None:
        if self.status != StockItemStatus.ARCHIVED:
            raise StockItemDeletionForbiddenError
