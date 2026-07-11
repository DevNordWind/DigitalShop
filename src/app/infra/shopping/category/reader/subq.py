from sqlalchemy import exists, func, select

from app.infra.framework.sql_alchemy.table.category import category_table
from app.infra.framework.sql_alchemy.table.position import (
    fixed_item_table,
    position_table,
    stock_item_table,
)

POSITIONS_COUNT_SUBQ = (
    select(func.count(position_table.c.id))
    .where(position_table.c.category_id == category_table.c.id)
    .correlate(category_table)
    .scalar_subquery()
).label("positions_amount")

_FIXED_ITEMS_COUNT = (
    select(func.count(fixed_item_table.c.id))
    .select_from(
        fixed_item_table.join(
            position_table,
            fixed_item_table.c.position_id == position_table.c.id,
        )
    )
    .where(position_table.c.category_id == category_table.c.id)
    .correlate(category_table)
    .scalar_subquery()
)

_STOCK_ITEMS_COUNT = (
    select(func.count(stock_item_table.c.id))
    .select_from(
        stock_item_table.join(
            position_table,
            stock_item_table.c.position_id == position_table.c.id,
        )
    )
    .where(position_table.c.category_id == category_table.c.id)
    .correlate(category_table)
    .scalar_subquery()
)

ITEMS_COUNT_SUBQ = (_FIXED_ITEMS_COUNT + _STOCK_ITEMS_COUNT).label("items_amount")

CATEGORY_HAS_POSITIONS_SUBQ = exists().where(
    position_table.c.category_id == category_table.c.id
)
