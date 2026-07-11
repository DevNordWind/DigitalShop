from typing import override
from uuid import UUID

from sqlalchemy import UUID as SaUUID  # noqa: N811
from sqlalchemy import Dialect, TypeDecorator

from app.domain.user.value_object import UserId


class UserIdType(TypeDecorator[UserId]):
    impl = SaUUID
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: UserId | None,
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
    ) -> UserId | None:
        if value is None:
            return None

        return UserId(value=value)
