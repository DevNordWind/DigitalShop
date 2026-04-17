from typing import Any

from sqlalchemy import Column

from infra.framework.sql_alchemy.table.payment import payment_table

PAYMENT_SELECT: tuple[Column[Any], ...] = (
    payment_table.c.id,
    payment_table.c.creator_id,
    payment_table.c.purpose_reference_id,
    payment_table.c.purpose_type,
    payment_table.c.original_amount_amount,
    payment_table.c.original_amount_currency,
    payment_table.c.to_pay_amount,
    payment_table.c.commission_type,
    payment_table.c.commission_coefficient,
    payment_table.c.commission_amount,
    payment_table.c.method,
    payment_table.c.status,
    payment_table.c.external_id,
    payment_table.c.created_at,
    payment_table.c.updated_at,
)
