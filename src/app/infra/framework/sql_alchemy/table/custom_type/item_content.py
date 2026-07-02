from typing import override

from sqlalchemy import Dialect, String, TypeDecorator

from app.domain.shopping.position.item.value_object import ItemContent


class ItemContentType(TypeDecorator[ItemContent]):
    impl = String(length=1024)
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: ItemContent | None,
        dialect: Dialect,
    ) -> str | None:
        if value is None:
            return None

        return value.value

    @override
    def process_result_value(
        self,
        value: str | None,
        dialect: Dialect,
    ) -> ItemContent | None:
        if value is None:
            return None

        return ItemContent(value=value)
