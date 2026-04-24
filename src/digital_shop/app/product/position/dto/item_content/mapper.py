from typing import TypeVar

from app.product.position.dto.item_content.dto import (
    ItemContentDTO,
    ItemRawDTO,
)
from domain.product.position.item.enums import ItemContentType
from domain.product.position.item.value_object import (
    ItemContent,
    ItemRaw,
    TextItem,
    TextItemRaw,
)

T = TypeVar("T")


class ItemRawMapper:
    @classmethod
    def to_value_object(cls, src: ItemRawDTO) -> ItemRaw:
        return TextItemRaw(value=src.value)


class ItemContentMapper:
    @classmethod
    def to_dto(cls, src: ItemContent) -> ItemContentDTO:
        tp: ItemContentType = src.type
        if isinstance(src, TextItem):
            return ItemContentDTO(value=src.value, type=tp)

        raise ValueError
