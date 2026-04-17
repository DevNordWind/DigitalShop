from dataclasses import dataclass
from uuid import UUID

from domain.common.localized import LocalizedText
from domain.product.position.value_object import PositionPrice


@dataclass(slots=True, frozen=True)
class PositionSnapshot:
    category_id: UUID
    position_id: UUID

    position_name: LocalizedText
    price: PositionPrice
