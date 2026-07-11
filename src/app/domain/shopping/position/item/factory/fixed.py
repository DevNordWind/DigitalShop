from app.domain.common.port import Clock, UUIDProvider
from app.domain.shopping.position.item.entity import FixedItem
from app.domain.shopping.position.item.enums import FixedItemStatus
from app.domain.shopping.position.item.value_object import FixedItemId, ItemContent
from app.domain.shopping.position.value_object import PositionId
from app.domain.user.value_object import UserId


class FixedItemFactory:
    def __init__(self, clock: Clock, uuid_provider: UUIDProvider):
        self._clock = clock
        self._uuid = uuid_provider

    def create(
        self, creator_id: UserId, position_id: PositionId, content: ItemContent
    ) -> FixedItem:
        return FixedItem(
            id=FixedItemId(self._uuid()),
            position_id=position_id,
            creator_id=creator_id,
            content=content,
            status=FixedItemStatus.AVAILABLE,
            created_at=self._clock.now(),
        )
