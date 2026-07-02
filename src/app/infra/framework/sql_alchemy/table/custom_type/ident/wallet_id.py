from typing import override
from uuid import UUID

from sqlalchemy import UUID as SaUUID  # noqa: N811
from sqlalchemy import Dialect, TypeDecorator

from app.domain.wallet.value_object import WalletId


class WalletIdType(TypeDecorator[WalletId]):
    impl = SaUUID
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: WalletId | None,
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
    ) -> WalletId | None:
        if value is None:
            return None

        return WalletId(value=value)
