from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import (
    ARRAY,
    NUMERIC,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Table,
    event,
)
from sqlalchemy import (
    UUID as SaUUID,  # noqa: N811
)
from sqlalchemy.orm import Composite, attributes

from domain.common.money import Currency, Money
from domain.coupon.value_object import CouponId
from domain.order.entity import Order
from domain.order.enums import OrderStatus, PaymentSourceType
from domain.order.value_object import AppliedCoupon, OrderId
from domain.order.value_object.source import PaymentSource
from domain.payment.value_object import PaymentId
from domain.product.position.item.value_object.items_amount import ItemsAmount
from domain.user.value_object import UserId

from .base import mapper_registry, metadata
from .custom_type import PositionSnapshotType
from .custom_type.item_snapshot import ItemSnapshotType

order_table: Table = Table(
    "Order",
    metadata,
    Column("id", SaUUID, primary_key=True),
    Column("customer_id", ForeignKey("User.id"), nullable=False, index=True),
    Column(
        "sub_total_amount",
        NUMERIC(19, 4),
        nullable=False,
    ),
    Column("sub_total_currency", Enum(Currency), nullable=False),
    Column("status", Enum(OrderStatus), nullable=False),
    Column("source_type", Enum(PaymentSourceType), nullable=True),
    Column("source_payment_id", ForeignKey("Payment.id"), nullable=True),
    Column("position", PositionSnapshotType(), nullable=False),
    Column("items", ARRAY(ItemSnapshotType(), as_tuple=True), nullable=True),
    Column("items_amount", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("confirmed_at", DateTime(timezone=True), nullable=True),
    Column("failed_at", DateTime(timezone=True), nullable=True),
    Column("expired_at", DateTime(timezone=True), nullable=True),
    Column("awaited_payment_at", DateTime(timezone=True), nullable=True),
    Column("cancelled_at", DateTime(timezone=True), nullable=True),
    Column("applied_coupon_id", ForeignKey("Coupon.id"), nullable=True),
    Column("discount_amount", NUMERIC(19, 4), nullable=True),
    Column("discount_currency", Enum(Currency), nullable=True),
    Column("total_amount", NUMERIC(19, 4), nullable=False),
    Column("total_currency", Enum(Currency), nullable=False),
)


def compose_payment_source(
    payment_id: UUID | None,
    tp: PaymentSourceType | None,
) -> PaymentSource | None:
    if payment_id is None and tp is None:
        return None

    if tp is None:
        return None

    return PaymentSource(
        payment_id=PaymentId(value=payment_id)
        if payment_id is not None
        else None,
        type=tp,
    )


def source_accessor(obj: object) -> tuple[object, ...]:
    return (
        obj.payment_id.value if obj.payment_id is not None else None,  # type: ignore[attr-defined]
        obj.type,  # type: ignore[attr-defined]
    )


composite_source = Composite(
    compose_payment_source,
    order_table.c.source_payment_id,
    order_table.c.source_type,
)
composite_source._generated_composite_accessor = source_accessor  # noqa: SLF001


def compose_applied_coupon(
    coupon_id: UUID | None,
    discount_amount: Decimal | None,
    discount_currency: Currency | None,
) -> AppliedCoupon | None:
    if (
        coupon_id is None
        or discount_amount is None
        or discount_currency is None
    ):
        return None

    return AppliedCoupon(
        coupon_id=CouponId(value=coupon_id),
        discount=Money(amount=discount_amount, currency=discount_currency),
    )


composite_coupon = Composite(
    compose_applied_coupon,
    order_table.c.applied_coupon_id,
    order_table.c.discount_amount,
    order_table.c.discount_currency,
)
composite_coupon._generated_composite_accessor = lambda obj: (  # noqa: SLF001
    obj.coupon_id.value,  # type: ignore[union-attr]
    obj.discount.amount,  # type: ignore[union-attr]
    obj.discount.currency,  # type: ignore[union-attr]
)


def calculate_total(_: Any, __: Any, target: Order) -> None:
    total = target.total

    target.__dict__["_total_amount"] = total.amount
    target.__dict__["_total_currency"] = total.currency
    attributes.flag_modified(target, "_total_amount")
    attributes.flag_modified(target, "_total_currency")


def map_order() -> None:
    mapper_registry.map_imperatively(
        Order,
        order_table,
        properties={
            "id": Composite(OrderId, order_table.c.id),
            "_id": order_table.c.id,
            "customer_id": Composite(UserId, order_table.c.customer_id),
            "_customer_id": order_table.c.customer_id,
            "sub_total": Composite(
                Money,
                order_table.c.sub_total_amount,
                order_table.c.sub_total_currency,
            ),
            "source": composite_source,
            "applied_coupon": composite_coupon,
            "_total_amount": order_table.c.total_amount,
            "_total_currency": order_table.c.total_currency,
            "items_amount": Composite(ItemsAmount, order_table.c.items_amount),
            "_items_amount": order_table.c.items_amount,
        },
    )
    event.listen(Order, "before_insert", calculate_total)
    event.listen(Order, "before_update", calculate_total)
