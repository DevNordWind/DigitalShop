from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class OrderId:
    value: UUID
