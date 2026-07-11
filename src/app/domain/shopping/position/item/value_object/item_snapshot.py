from dataclasses import dataclass
from uuid import UUID

from app.domain.shopping.position.item.value_object.item_content import ItemContent


@dataclass(slots=True, frozen=True)
class ItemSnapshot:
    id: UUID
    content: ItemContent
