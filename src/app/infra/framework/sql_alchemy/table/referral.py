from decimal import Decimal
from uuid import UUID

from sqlalchemy import UUID as SaUUID  # noqa: N811
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    Table,
)
from sqlalchemy.orm import composite

from app.domain.common.money import Currency, Money
from app.domain.referral.entity import ReferralAward, ReferrerProfile
from app.domain.referral.enums import ReferralAwardSourceType
from app.domain.referral.enums.status import ReferralAwardStatus
from app.domain.referral.policy import ReferralPolicy
from app.domain.referral.value_object import ReferralAwardSource

from .base import mapper_registry, metadata
from .custom_type import (
    CoefficientType,
    ExchangeRateType,
    ReferralAwardIdType,
    UserIdType,
)

referral_award_table: Table = Table(
    "ReferralAward",
    metadata,
    Column("id", ReferralAwardIdType, primary_key=True),
    Column(
        "referrer_id", UserIdType, ForeignKey("User.id"), nullable=False, index=True
    ),
    Column("status", Enum(ReferralAwardStatus), nullable=False),
    Column("source_reference_id", SaUUID, nullable=False),
    Column("source_type", Enum(ReferralAwardSourceType), nullable=False),
    Column("source_amount", Numeric(19, 4), nullable=False),
    Column("source_currency", Enum(Currency), nullable=False),
    Column(
        "coefficient_snapshot",
        CoefficientType,
        nullable=False,
    ),
    Column("award_amount", Numeric(19, 4), nullable=True),
    Column("award_currency", Enum(Currency), nullable=True),
    Column("exchange_rate_snapshot", ExchangeRateType(), nullable=True),
    Column("completed_at", DateTime(timezone=True), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

referrer_profile_table: Table = Table(
    "ReferrerProfile",
    metadata,
    Column("user_id", UserIdType, ForeignKey("User.id"), primary_key=True),
    Column("award_currency", Enum(Currency), nullable=False),
    Column("send_notifications", Boolean, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

referral_policy_table: Table = Table(
    "ReferralPolicy",
    metadata,
    Column("current_version", Integer, primary_key=True),
    Column(
        "coefficient",
        CoefficientType,
        nullable=False,
    ),
)


def compose_award(
    amount: Decimal | None,
    currency: Currency | None,
) -> Money | None:
    if amount is None or currency is None:
        return None

    return Money(
        amount=amount,
        currency=currency,
    )


composite_award = composite(
    compose_award,
    referral_award_table.c.award_amount,
    referral_award_table.c.award_currency,
)
composite_award._generated_composite_accessor = lambda obj: (  # noqa: SLF001
    obj.amount,  # type: ignore[union-attr]
    obj.currency,  # type: ignore[union-attr]
)


def compose_source(
    reference_id: UUID,
    tp: ReferralAwardSourceType,
    amount: Decimal,
    currency: Currency,
) -> ReferralAwardSource:
    return ReferralAwardSource(
        reference_id=reference_id,
        type=tp,
        amount=Money(amount=amount, currency=currency),
    )


composite_source = composite(
    compose_source,
    referral_award_table.c.source_reference_id,
    referral_award_table.c.source_type,
    referral_award_table.c.source_amount,
    referral_award_table.c.source_currency,
)

composite_source._generated_composite_accessor = lambda obj: (  # noqa: SLF001
    obj.reference_id,
    obj.type,
    obj.amount.amount,
    obj.amount.currency,
)


def map_referral_award() -> None:
    mapper_registry.map_imperatively(
        ReferralAward,
        referral_award_table,
        properties={
            "source": composite_source,
            "award": composite_award,
        },
    )


def map_referrer_profile() -> None:
    mapper_registry.map_imperatively(
        ReferrerProfile,
        referrer_profile_table,
    )


def map_referral_policy() -> None:
    mapper_registry.map_imperatively(
        ReferralPolicy,
        referral_policy_table,
    )
