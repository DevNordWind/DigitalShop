from dataclasses import dataclass
from uuid import UUID

from domain.product.position.item.value_object import ItemContent


@dataclass(slots=True, frozen=True)
class ItemSnapshot:
    item_id: UUID
    item_content: ItemContent

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ItemSnapshot):
            return False

        return other.item_id == self.item_id

    def __hash__(self) -> int:
        return hash(self.item_id)
