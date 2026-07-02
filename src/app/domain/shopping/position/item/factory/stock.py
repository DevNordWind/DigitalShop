from collections.abc import Sequence

from app.domain.common.port import Clock, UUIDProvider
from app.domain.shopping.position.item.entity import StockItem
from app.domain.shopping.position.item.enums import StockItemStatus
from app.domain.shopping.position.item.value_object import (
    ItemContent,
    StockItemId,
)
from app.domain.shopping.position.value_object import PositionId
from app.domain.user.value_object import UserId


class StockItemFactory:
    def __init__(self, clock: Clock, uuid_provider: UUIDProvider):
        self._clock = clock
        self._uuid = uuid_provider

    def create(
        self,
        creator_id: UserId,
        position_id: PositionId,
        contents: Sequence[ItemContent],
    ) -> tuple[StockItem, ...]:
        now = self._clock.now()

        return tuple(
            StockItem(
                id=StockItemId(self._uuid()),
                position_id=position_id,
                creator_id=creator_id,
                content=content,
                status=StockItemStatus.AVAILABLE,
                created_at=now,
            )
            for content in contents
        )
