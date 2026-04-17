from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    Table,
)
from sqlalchemy.orm import Composite

from domain.coupon.entity import Coupon
from domain.coupon.entity.redemption import CouponRedemption
from domain.coupon.enums import CouponRedemptionStatus
from domain.coupon.value_object import CouponCode, CouponId, CouponRedemptionId
from domain.order.value_object import OrderId
from domain.user.value_object import UserId

from .base import mapper_registry, metadata
from .custom_type import CouponValidityType, DiscountStrategyType

coupon_table: Table = Table(
    "Coupon",
    metadata,
    Column(
        "id",
        UUID,
        primary_key=True,
    ),
    Column("creator_id", ForeignKey("User.id"), nullable=False),
    Column("code", String(length=64), nullable=False, unique=True),
    Column(
        "discount",
        DiscountStrategyType,
        nullable=False,
    ),
    Column("valid_from", CouponValidityType(), nullable=False),
    Column("valid_until", CouponValidityType(), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("is_revoked", Boolean, nullable=False),
)

coupon_redemption_table: Table = Table(
    "CouponRedemption",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("coupon_id", ForeignKey("Coupon.id"), nullable=False),
    Column("user_id", ForeignKey("User.id"), nullable=False),
    Column("order_id", ForeignKey("Order.id"), nullable=False),
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
        properties={
            "id": Composite(CouponId, coupon_table.c.id),
            "_id": coupon_table.c.id,
            "creator_id": Composite(UserId, coupon_table.c.creator_id),
            "_creator_id": coupon_table.c.creator_id,
            "code": Composite(CouponCode, coupon_table.c.code),
            "_code": coupon_table.c.code,
        },
    )


def map_coupon_redemption() -> None:
    mapper_registry.map_imperatively(
        CouponRedemption,
        coupon_redemption_table,
        properties={
            "id": Composite(CouponRedemptionId, coupon_redemption_table.c.id),
            "_id": coupon_redemption_table.c.id,
            "coupon_id": Composite(
                CouponId,
                coupon_redemption_table.c.coupon_id,
            ),
            "_coupon_id": coupon_redemption_table.c.coupon_id,
            "user_id": Composite(UserId, coupon_redemption_table.c.user_id),
            "_user_id": coupon_redemption_table.c.user_id,
            "order_id": Composite(OrderId, coupon_redemption_table.c.order_id),
            "_order_id": coupon_redemption_table.c.order_id,
        },
    )
