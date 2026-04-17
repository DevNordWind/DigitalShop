from typing import TypeVar

from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB

from domain.product.position.item.value_object import (
    ItemContent,
    TextItem,
)

T = TypeVar("T")


class ItemContentDeserializationError(Exception):
    pass


class ItemContentType(TypeDecorator[ItemContent]):
    impl = JSONB
    cache_ok = True

    def process_bind_param(
        self,
        value: ItemContent | None,
        dialect: Dialect,
    ) -> dict[str, str | dict[str, str]] | None:
        if value is None:
            return None
        if isinstance(value.value, str):
            return {"value": value.value}
        raise ItemContentDeserializationError(
            f"Unsupported ItemContent type: {type(value.value)}",
        )

    def process_result_value(
        self,
        value: dict[str, str | dict[str, str]] | None,
        dialect: Dialect,
    ) -> ItemContent | None:
        if value is None:
            return None
        try:
            inner = value["value"]
        except KeyError as e:
            raise ItemContentDeserializationError(
                f"Missing 'value' key in stored data: {value}",
            ) from e
        if isinstance(inner, str):
            return TextItem(value=inner)
        raise ItemContentDeserializationError(
            f"Unexpected 'value' type in stored data: {type(inner)}",
        )
