from dataclasses import dataclass
from uuid import UUID

from app.domain.common.localized import LocalizedText
from app.domain.shopping.position.value_object import PositionPrice


@dataclass(slots=True, frozen=True)
class PositionSnapshot:
    category_id: UUID
    position_id: UUID
    price: PositionPrice

    position_name: LocalizedText
