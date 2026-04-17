from datetime import datetime
from typing import TypeVar

from domain.common.file import FileKeyRaw
from domain.common.port import Clock, UUIDProvider
from domain.product.category.entity import Category
from domain.product.category.exception import CategoryArchived
from domain.product.position.entity import Position
from domain.product.position.enums.warehouse import WarehouseType
from domain.product.position.exception import (
    PositionPermissionDenied,
)
from domain.product.position.item.entity import Item
from domain.product.position.item.factory import ItemFactory
from domain.product.position.service.access_service import (
    PositionAccessService,
)
from domain.product.position.service.media_key_factory import (
    PositionMediaKeyFactory,
)
from domain.product.position.service.warehouse_factory import (
    WarehouseFactory,
)
from domain.product.position.strategy import (
    WarehouseStrategy,
)
from domain.product.position.value_object import (
    PositionDescription,
    PositionId,
    PositionMediaKey,
    PositionName,
    PositionPrice,
)
from domain.user.entity import User

T = TypeVar("T", bound=Item)


class PositionService:
    def __init__(
        self,
        uuid_provider: UUIDProvider,
        clock: Clock,
        media_key_factory: PositionMediaKeyFactory,
        item_factory: ItemFactory,
    ):
        self._uuid: UUIDProvider = uuid_provider
        self._clock: Clock = clock
        self._media_key_factory: PositionMediaKeyFactory = media_key_factory
        self._item_factory: ItemFactory = item_factory

    def create(
        self,
        category: Category,
        creator: User,
        name: PositionName,
        description: PositionDescription | None,
        media_raw: list[FileKeyRaw],
        warehouse_type: WarehouseType,
        price: PositionPrice,
    ) -> Position:
        category.ensure_can_add_positions()

        if not PositionAccessService.can_create(creator_role=creator.role):
            raise PositionPermissionDenied

        position_id = PositionId(self._uuid())
        now: datetime = self._clock.now()

        warehouse: WarehouseStrategy = WarehouseFactory.create(
            tp=warehouse_type,
        )

        media: list[PositionMediaKey] = [
            self._media_key_factory.generate(category.id, position_id, raw)
            for raw in media_raw
        ]

        return Position(
            id=position_id,
            category_id=category.id,
            creator_id=creator.id,
            name=name,
            description=description,
            media=media,
            warehouse=warehouse,
            price=price,
            created_at=now,
            updated_at=None,
            archived_at=None,
        )

    def recover(self, category: Category, position: Position) -> None:
        if category.is_archived:
            raise CategoryArchived

        position.recover(now=self._clock.now())
