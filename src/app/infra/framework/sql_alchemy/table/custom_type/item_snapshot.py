from typing import override
from uuid import UUID

from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB

from app.domain.shopping.position.item.value_object import ItemContent, ItemSnapshot


class ItemSnapshotType(TypeDecorator[ItemSnapshot]):
    impl = JSONB
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: ItemSnapshot | None,
        dialect: Dialect,
    ) -> dict[str, str] | None:
        if value is None:
            return None

        return {
            "id": value.id.hex,
            "content": value.content.value,
        }

    @override
    def process_result_value(
        self,
        value: dict[str, str] | None,
        dialect: Dialect,
    ) -> ItemSnapshot | None:
        if value is None:
            return None

        return ItemSnapshot(
            id=UUID(value["id"]),
            content=ItemContent(value["content"]),
        )
