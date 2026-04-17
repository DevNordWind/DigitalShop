from datetime import datetime

from domain.common.port import UUIDProvider
from domain.product.position.entity import Position
from domain.product.position.item.entity import FiniteItem, InfiniteItem, Item
from domain.product.position.item.enums import ItemStatus
from domain.product.position.item.factory.item_content import (
    ItemContentFactory,
)
from domain.product.position.item.value_object import ItemId, ItemRaw
from domain.product.position.strategy import FiniteWarehouse, InfiniteWarehouse
from domain.user.value_object import UserId


class ItemFactory:
    def __init__(
        self,
        uuid_provider: UUIDProvider,
        content_factory: ItemContentFactory,
    ):
        self._uuid: UUIDProvider = uuid_provider
        self._content_factory: ItemContentFactory = content_factory

    def create(
        self,
        position: Position,
        creator_id: UserId,
        item_raw: ItemRaw,
        now: datetime,
    ) -> Item:
        item_id = ItemId(self._uuid())
        item_content = self._content_factory.create(
            raw=item_raw,
        )

        match position.warehouse:
            case InfiniteWarehouse():
                return InfiniteItem(
                    id=item_id,
                    position_id=position.id,
                    creator_id=creator_id,
                    content=item_content,
                    created_at=now,
                    status=ItemStatus.AVAILABLE,
                    archived_at=None,
                    updated_at=None,
                )
            case FiniteWarehouse():
                return FiniteItem(
                    id=item_id,
                    position_id=position.id,
                    creator_id=creator_id,
                    content=item_content,
                    status=ItemStatus.AVAILABLE,
                    created_at=now,
                    archived_at=None,
                    updated_at=None,
                )
            case _:
                raise ValueError(
                    f"Unknown position Warehouse: {position.warehouse.__class__.__name__}",  # noqa: E501
                )
