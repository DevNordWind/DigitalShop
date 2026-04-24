from dataclasses import dataclass

from domain.product.position.item.enums import ItemContentType


@dataclass(slots=True, frozen=True)
class ItemRawDTO:
    value: str


@dataclass(slots=True, frozen=True)
class ItemContentDTO:
    value: str
    type: ItemContentType
