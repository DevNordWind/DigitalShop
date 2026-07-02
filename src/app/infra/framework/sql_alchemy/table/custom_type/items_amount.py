from typing import override

from sqlalchemy import Dialect, Integer, TypeDecorator

from app.domain.shopping.position.item.value_object import ItemsAmount


class ItemsAmountType(TypeDecorator[ItemsAmount]):
    impl = Integer
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: ItemsAmount | None,
        dialect: Dialect,
    ) -> int | None:
        if value is None:
            return None

        return value.value

    @override
    def process_result_value(
        self,
        value: int | None,
        dialect: Dialect,
    ) -> ItemsAmount | None:
        if value is None:
            return None

        return ItemsAmount(value=value)
