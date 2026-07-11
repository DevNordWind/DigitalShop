from decimal import Decimal
from typing import Any, override
from uuid import UUID

from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB

from app.domain.common.money import Currency, Money
from app.domain.referral.enums import (
    ReferralAwardSourceType as EnumReferralAwardSourceType,
)
from app.domain.referral.value_object import ReferralAwardSource


class ReferralAwardSourceType(TypeDecorator[ReferralAwardSource]):
    impl = JSONB
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: ReferralAwardSource | None,
        dialect: Dialect,
    ) -> dict[str, Any] | None:
        if value is None:
            return None
        return {
            "reference_id": str(value.reference_id),
            "type": value.type.value,
            "amount": str(value.amount.amount),
            "currency": value.amount.currency.value,
        }

    @override
    def process_result_value(
        self,
        value: dict[str, Any] | None,
        dialect: Dialect,
    ) -> ReferralAwardSource | None:
        if value is None:
            return None

        return ReferralAwardSource(
            reference_id=UUID(value["reference_id"]),
            type=EnumReferralAwardSourceType(value["type"]),
            amount=Money(
                amount=Decimal(value["amount"]),
                currency=Currency(value["currency"]),
            ),
        )
