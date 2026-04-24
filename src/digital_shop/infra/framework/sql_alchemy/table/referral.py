from decimal import Decimal
from uuid import UUID

from domain.common.coefficient import Coefficient
from domain.common.money import Currency, Money
from domain.referral.entity import ReferralAward, ReferrerProfile
from domain.referral.enums import ReferralAwardSourceType
from domain.referral.enums.status import ReferralAwardStatus
from domain.referral.policy import ReferralPolicy
from domain.referral.value_object import ReferralAwardId, ReferralAwardSource
from domain.user.value_object import UserId
from sqlalchemy import (
    UUID as SaUUID,  # noqa: N811
)
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
from sqlalchemy.orm import Composite

from .base import mapper_registry, metadata
from .custom_type import (
    ExchangeRateType,
)

referral_award_table: Table = Table(
    "ReferralAward",
    metadata,
    Column("id", SaUUID, primary_key=True),
    Column("referrer_id", ForeignKey("User.id"), nullable=False, index=True),
    Column("status", Enum(ReferralAwardStatus), nullable=False),
    Column("source_reference_id", SaUUID, nullable=False),
    Column("source_type", Enum(ReferralAwardSourceType), nullable=False),
    Column("source_amount", Numeric(19, 4), nullable=False),
    Column("source_currency", Enum(Currency), nullable=False),
    Column(
        "coefficient_snapshot",
        Numeric(precision=4, scale=3),
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
    Column("user_id", ForeignKey("User.id"), primary_key=True),
    Column("award_currency", Enum(Currency), nullable=False),
    Column("send_notifications", Boolean, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

referral_policy_table: Table = Table(
    "ReferralPolicy",
    metadata,
    Column("current_version", Integer, primary_key=True),
    Column("coefficient", Numeric(precision=4, scale=3), nullable=False),
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


composite_award = Composite(
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


composite_source = Composite(
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
            "id": Composite(ReferralAwardId, referral_award_table.c.id),
            "_id": referral_award_table.c.id,
            "referrer_id": Composite(
                UserId,
                referral_award_table.c.referrer_id,
            ),
            "_referrer_id": referral_award_table.c.referrer_id,
            "source": composite_source,
            "award": composite_award,
            "coefficient_snapshot": Composite(
                Coefficient,
                referral_award_table.c.coefficient_snapshot,
            ),
            "_coefficient_snapshot": referral_award_table.c.coefficient_snapshot,  # noqa: E501
        },
    )


def map_referrer_profile() -> None:
    mapper_registry.map_imperatively(
        ReferrerProfile,
        referrer_profile_table,
        properties={
            "user_id": Composite(UserId, referrer_profile_table.c.user_id),
            "_user_id": referrer_profile_table.c.user_id,
        },
    )


def map_referral_policy() -> None:
    mapper_registry.map_imperatively(
        ReferralPolicy,
        referral_policy_table,
        properties={
            "coefficient": Composite(
                Coefficient,
                referral_policy_table.c.coefficient,
            ),
            "_coefficient": referral_policy_table.c.coefficient,
        },
    )
