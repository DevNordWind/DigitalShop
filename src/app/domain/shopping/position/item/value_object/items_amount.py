from dataclasses import dataclass

from app.domain.shopping.position.item.exception import (
    NegativeItemsAmountForbiddenError,
)


@dataclass(slots=True, frozen=True)
class ItemsAmount:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise NegativeItemsAmountForbiddenError
