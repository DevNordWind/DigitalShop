from typing import override
from uuid import UUID

from sqlalchemy import UUID as SaUUID  # noqa: N811
from sqlalchemy import Dialect, TypeDecorator

from app.domain.shopping.position.item.value_object import FixedItemId, StockItemId


class FixedItemIdType(TypeDecorator[FixedItemId]):
    impl = SaUUID
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: FixedItemId | None,
        dialect: Dialect,
    ) -> UUID | None:
        if value is None:
            return None

        return value.value

    @override
    def process_result_value(
        self,
        value: UUID | None,
        dialect: Dialect,
    ) -> FixedItemId | None:
        if value is None:
            return None

        return FixedItemId(value=value)


class StockItemIdType(TypeDecorator[StockItemId]):
    impl = SaUUID
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: StockItemId | None,
        dialect: Dialect,
    ) -> UUID | None:
        if value is None:
            return None

        return value.value

    @override
    def process_result_value(
        self,
        value: UUID | None,
        dialect: Dialect,
    ) -> StockItemId | None:
        if value is None:
            return None

        return StockItemId(value=value)
