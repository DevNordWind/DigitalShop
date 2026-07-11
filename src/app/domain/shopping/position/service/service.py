from datetime import datetime

from app.domain.common.file_key import FileKeyRaw
from app.domain.common.port import Clock, UUIDProvider
from app.domain.shopping.category.entity import Category
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.enums import FulfillmentType, WarehouseType
from app.domain.shopping.position.factory import PositionMediaKeyFactory
from app.domain.shopping.position.value_object import (
    PositionDescription,
    PositionId,
    PositionMediaKey,
    PositionName,
    PositionPrice,
)
from app.domain.user.value_object import UserId


class PositionDomainService:
    def __init__(
        self,
        uuid_provider: UUIDProvider,
        clock: Clock,
        media_key_factory: PositionMediaKeyFactory,
    ):
        self._uuid: UUIDProvider = uuid_provider
        self._clock: Clock = clock
        self._media_key_factory: PositionMediaKeyFactory = media_key_factory

    def create(
        self,
        category: Category,
        creator_id: UserId,
        name: PositionName,
        description: PositionDescription | None,
        media_raw: list[FileKeyRaw],
        warehouse_type: WarehouseType,
        fulfillment_type: FulfillmentType,
        price: PositionPrice,
    ) -> Position:
        category.ensure_can_add_positions()

        position_id = PositionId(self._uuid())
        now: datetime = self._clock.now()

        media: list[PositionMediaKey] = [
            self._media_key_factory.generate(category.id, position_id, raw)
            for raw in media_raw
        ]

        return Position(
            id=position_id,
            category_id=category.id,
            creator_id=creator_id,
            name=name,
            description=description,
            media=media,
            price=price,
            warehouse_type=warehouse_type,
            fulfillment_type=fulfillment_type,
            created_at=now,
            updated_at=None,
            archived_at=None,
        )
