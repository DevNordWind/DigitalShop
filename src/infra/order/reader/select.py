from typing import Any

from sqlalchemy import Column, Label

from infra.framework.sql_alchemy.table.coupon import coupon_table
from infra.framework.sql_alchemy.table.order import order_table
from infra.framework.sql_alchemy.table.payment import payment_table

ORDER_SELECT: tuple[Column[Any] | Label[Any], ...] = (
    order_table.c.id,
    order_table.c.customer_id,
    order_table.c.sub_total_amount,
    order_table.c.sub_total_currency,
    order_table.c.status,
    order_table.c.source_type,
    order_table.c.source_payment_id,
    order_table.c.position,
    order_table.c["items"],
    order_table.c.items_amount,
    order_table.c.created_at,
    order_table.c.confirmed_at,
    order_table.c.awaited_payment_at,
    order_table.c.failed_at,
    order_table.c.cancelled_at,
    order_table.c.applied_coupon_id,
    order_table.c.discount_amount,
    order_table.c.discount_currency,
    order_table.c.total_amount,
    order_table.c.total_currency,
    coupon_table.c.id.label("coupon_id"),
    coupon_table.c.creator_id.label("coupon_creator_id"),
    coupon_table.c.code.label("coupon_code"),
    coupon_table.c.discount.label("coupon_discount"),
    coupon_table.c.valid_from.label("coupon_valid_from"),
    coupon_table.c.valid_until.label("coupon_valid_until"),
    coupon_table.c.created_at.label("coupon_created_at"),
    coupon_table.c.is_revoked.label("coupon_is_revoked"),
    payment_table.c.method.label("payment_method"),
)
