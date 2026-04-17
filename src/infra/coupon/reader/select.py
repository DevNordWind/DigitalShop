from typing import Any

from sqlalchemy import Column

from infra.framework.sql_alchemy.table.coupon import coupon_table

COUPON_SELECT: tuple[Column[Any], ...] = (
    coupon_table.c.id,
    coupon_table.c.creator_id,
    coupon_table.c.code,
    coupon_table.c.discount,
    coupon_table.c.valid_from,
    coupon_table.c.valid_until,
    coupon_table.c.created_at,
    coupon_table.c.is_revoked,
)
