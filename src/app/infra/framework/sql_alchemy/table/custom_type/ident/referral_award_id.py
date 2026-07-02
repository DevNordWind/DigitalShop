from typing import override
from uuid import UUID

from sqlalchemy import UUID as SaUUID  # noqa: N811
from sqlalchemy import Dialect, TypeDecorator

from app.domain.referral.value_object import ReferralAwardId


class ReferralAwardIdType(TypeDecorator[ReferralAwardId]):
    impl = SaUUID
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: ReferralAwardId | None,
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
    ) -> ReferralAwardId | None:
        if value is None:
            return None

        return ReferralAwardId(value=value)
