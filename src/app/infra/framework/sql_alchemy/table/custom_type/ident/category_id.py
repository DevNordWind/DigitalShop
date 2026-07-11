from typing import override
from uuid import UUID

from sqlalchemy import UUID as SaUUID  # noqa: N811
from sqlalchemy import Dialect, TypeDecorator

from app.domain.shopping.category.value_object import CategoryId


class CategoryIdType(TypeDecorator[CategoryId]):
    impl = SaUUID
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: CategoryId | None,
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
    ) -> CategoryId | None:
        if value is None:
            return None

        return CategoryId(value=value)
