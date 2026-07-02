from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class StockItemId:
    value: UUID


@dataclass(slots=True, frozen=True)
class FixedItemId:
    value: UUID
