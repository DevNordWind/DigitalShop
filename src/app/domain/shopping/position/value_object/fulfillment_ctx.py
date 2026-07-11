from dataclasses import dataclass
from datetime import datetime

from app.domain.shopping.position.item.value_object import ItemsAmount


@dataclass(slots=True, frozen=True)
class HoldContext:
    now: datetime
    amount: ItemsAmount


@dataclass(slots=True, frozen=True)
class SellContext:
    now: datetime
