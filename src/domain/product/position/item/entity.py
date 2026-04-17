from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from domain.product.position.item.enums import (
    ItemStatus,
)
from domain.product.position.item.exception import (
    ItemContentReplaceForbidden,
    ItemDeletionForbidden,
    ItemReleaseForbidden,
    ItemReservationForbidden,
    ItemSellForbidden,
)
from domain.product.position.item.value_object import (
    ItemContent,
    ItemId,
)
from domain.product.position.value_object import PositionId
from domain.user.value_object import UserId


@dataclass(kw_only=True)
class Item(ABC):
    id: ItemId
    position_id: PositionId
    creator_id: UserId

    content: ItemContent
    status: ItemStatus

    created_at: datetime
    archived_at: datetime | None
    updated_at: datetime | None

    @property
    def is_archived(self) -> bool:
        return (
            self.status == ItemStatus.ARCHIVED and self.archived_at is not None
        )

    def archive(self, now: datetime) -> None:
        if self.is_archived:
            return

        self.archived_at = now
        self.status = ItemStatus.ARCHIVED

    def recover(self) -> None:
        if not self.is_archived:
            return

        self.status = ItemStatus.AVAILABLE
        self.archived_at = None

    def replace_content(
        self,
        new_content: ItemContent,
        now: datetime,
    ) -> ItemContent | None:
        if new_content == self.content:
            return None

        self._ensure_content_replaceable()
        old_content = self.content

        self.content = new_content
        self.updated_at = now

        return old_content

    def ensure_can_delete(self) -> None:
        if not self.is_archived:
            raise ItemDeletionForbidden

    @abstractmethod
    def _ensure_content_replaceable(self) -> None:
        raise NotImplementedError


@dataclass(kw_only=True)
class InfiniteItem(Item):
    status: Literal[ItemStatus.AVAILABLE, ItemStatus.ARCHIVED]

    def _ensure_content_replaceable(self) -> None:
        if self.is_archived:
            raise ItemContentReplaceForbidden


@dataclass(kw_only=True)
class FiniteItem(Item):
    status: ItemStatus

    sold_at: datetime | None = None
    reserved_at: datetime | None = None

    @property
    def is_available(self) -> bool:
        return self.status == ItemStatus.AVAILABLE

    @property
    def is_reserved(self) -> bool:
        return (
            self.status == ItemStatus.RESERVED and self.reserved_at is not None
        )

    @property
    def is_sold(self) -> bool:
        return self.status == ItemStatus.SOLD and self.sold_at is not None

    def reserve(self, now: datetime) -> None:
        if not self.is_available:
            raise ItemReservationForbidden

        self.status = ItemStatus.RESERVED
        self.reserved_at = now

    def release(self) -> None:
        if not self.is_reserved:
            raise ItemReleaseForbidden

        self.status = ItemStatus.AVAILABLE
        self.reserved_at = None

    def sell_direct(self, now: datetime) -> None:
        if not self.is_available:
            raise ItemSellForbidden

        self.sold_at = now
        self.status = ItemStatus.SOLD

    def sell_reserved(self, now: datetime) -> None:
        if not self.is_reserved:
            raise ItemSellForbidden

        self.sold_at = now
        self.status = ItemStatus.SOLD

    def _ensure_content_replaceable(self) -> None:
        if not self.is_available:
            raise ItemContentReplaceForbidden
