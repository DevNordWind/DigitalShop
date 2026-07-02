from decimal import Decimal
from typing import Any

from sqlalchemy import ColumnElement, Label, ScalarSelect, exists, func, or_, select

from app.infra.framework.sql_alchemy.table.position import (
    fixed_item_table,
    position_table,
    stock_item_table,
)

_FIXED_ITEMS_COUNT: ScalarSelect[Any] = (
    select(func.count(fixed_item_table.c.id))
    .where(fixed_item_table.c.position_id == position_table.c.id)
    .correlate(position_table)
    .scalar_subquery()
)

_STOCK_ITEMS_COUNT: ScalarSelect[Any] = (
    select(func.count(stock_item_table.c.id))
    .where(stock_item_table.c.position_id == position_table.c.id)
    .correlate(position_table)
    .scalar_subquery()
)

ITEMS_COUNT_SUBQ: Label[int | float | Decimal | Any] = (
    _FIXED_ITEMS_COUNT + _STOCK_ITEMS_COUNT
).label("items_amount")

ITEM_EXISTS_SUBQ: ColumnElement[bool] = or_(
    exists().where(fixed_item_table.c.position_id == position_table.c.id),
    exists().where(stock_item_table.c.position_id == position_table.c.id),
)
