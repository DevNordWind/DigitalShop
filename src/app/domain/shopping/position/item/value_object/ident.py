from dataclasses import dataclass
from typing import Protocol, runtime_checkable
from uuid import UUID


@runtime_checkable
class HasValue(Protocol):
    value: UUID


@dataclass(slots=True, frozen=True)
class StockItemId:
    value: UUID

    def __gt__(self, other: HasValue | UUID) -> bool:
        if isinstance(other, UUID):
            return self.value > other
        if not isinstance(other, HasValue):
            return NotImplemented

        return self.value > other.value

    def __lt__(self, other: HasValue | UUID) -> bool:
        if isinstance(other, UUID):
            return self.value < other
        if not isinstance(other, HasValue):
            return NotImplemented

        return self.value < other.value


@dataclass(slots=True, frozen=True)
class FixedItemId:
    value: UUID

    def __gt__(self, other: HasValue | UUID) -> bool:
        if isinstance(other, UUID):
            return self.value > other
        if not isinstance(other, HasValue):
            return NotImplemented

        return self.value > other.value

    def __lt__(self, other: HasValue | UUID) -> bool:
        if isinstance(other, UUID):
            return self.value < other
        if not isinstance(other, HasValue):
            return NotImplemented

        return self.value < other.value
