from typing import override
from zoneinfo import ZoneInfo

from sqlalchemy import Dialect
from sqlalchemy.types import String, TypeDecorator


class ZoneInfoType(TypeDecorator[ZoneInfo]):
    impl = String(64)
    cache_ok = True

    @override
    def process_bind_param(
        self, value: ZoneInfo | None, dialect: Dialect
    ) -> str | None:
        if value is None:
            return None

        return value.key

    @override
    def process_result_value(
        self, value: str | None, dialect: Dialect
    ) -> ZoneInfo | None:
        if value is None:
            return None

        return ZoneInfo(value)
