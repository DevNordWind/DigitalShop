from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from app.domain.shopping.category.value_object import CategoryId
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.enums import PositionStatus
from app.domain.shopping.position.item.enums import GenericItemStatus
from app.domain.shopping.position.value_object import PositionId


class PositionRepository(ABC):
    @abstractmethod
    async def add(self, position: Position) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        position_id: PositionId,
    ) -> Position | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_item_id(
        self,
        item_id: UUID,
    ) -> Position | None:
        raise NotImplementedError

    @abstractmethod
    async def get_with_items_ids(
        self,
        position_id: PositionId,
        item_status: GenericItemStatus | None = None,
    ) -> tuple[Position | None, tuple[UUID, ...]]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_category_ids_status(
        self, category_ids: Sequence[CategoryId], status: PositionStatus | None = None
    ) -> list[Position]:
        raise NotImplementedError

    @abstractmethod
    async def acquire(self, position_id: PositionId) -> Position | None:
        raise NotImplementedError

    @abstractmethod
    async def acquire_by_category_ids_status(
        self, category_ids: Sequence[CategoryId], status: PositionStatus | None = None
    ) -> list[Position]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, position: Position) -> None:
        raise NotImplementedError
