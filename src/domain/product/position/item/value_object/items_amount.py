from dataclasses import dataclass

from domain.product.position.item.exception import NegativeItemsAmountError


@dataclass(slots=True, frozen=True)
class ItemsAmount:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise NegativeItemsAmountError
