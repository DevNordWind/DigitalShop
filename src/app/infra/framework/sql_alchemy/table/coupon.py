from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Table,
)

from app.domain.coupon.entity import Coupon, CouponRedemption
from app.domain.coupon.enums import CouponRedemptionStatus

from .base import mapper_registry, metadata
from .custom_type import (
    CouponCodeType,
    CouponIdType,
    CouponRedemptionIdType,
    CouponValidityType,
    DiscountStrategyType,
    OrderIdType,
    UserIdType,
)

coupon_table: Table = Table(
    "Coupon",
    metadata,
    Column("id", CouponIdType, primary_key=True),
    Column("creator_id", UserIdType, ForeignKey("User.id"), nullable=False),
    Column("code", CouponCodeType, nullable=False, unique=True),
    Column(
        "discount",
        DiscountStrategyType,
        nullable=False,
    ),
    Column("valid_from", CouponValidityType, nullable=False),
    Column("valid_until", CouponValidityType, nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("is_revoked", Boolean, nullable=False),
)

coupon_redemption_table: Table = Table(
    "CouponRedemption",
    metadata,
    Column("id", CouponRedemptionIdType, primary_key=True),
    Column("coupon_id", CouponIdType, ForeignKey("Coupon.id"), nullable=False),
    Column("user_id", UserIdType, ForeignKey("User.id"), nullable=False),
    Column("order_id", OrderIdType, ForeignKey("Order.id"), nullable=False),
    Column("status", Enum(CouponRedemptionStatus), nullable=False),
    Column("reserved_at", DateTime(timezone=True), nullable=False),
    Column("confirmed_at", DateTime(timezone=True), nullable=True),
    Column("cancelled_at", DateTime(timezone=True), nullable=True),
)
Index(
    "uq_coupon_user_not_cancelled",
    coupon_redemption_table.c.coupon_id,
    coupon_redemption_table.c.user_id,
    unique=True,
    postgresql_where=(
        coupon_redemption_table.c.status != CouponRedemptionStatus.CANCELLED
    ),
    _table=coupon_redemption_table,
)


def map_coupon() -> None:
    mapper_registry.map_imperatively(
        Coupon,
        coupon_table,
    )


def map_coupon_redemption() -> None:
    mapper_registry.map_imperatively(
        CouponRedemption,
        coupon_redemption_table,
    )
