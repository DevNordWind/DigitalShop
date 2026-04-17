from typing import Any

from sqlalchemy import ScalarSelect, func, select
from sqlalchemy.sql.selectable import Select

from infra.framework.sql_alchemy.table.category import category_table
from infra.framework.sql_alchemy.table.position import (
    item_table,
    position_table,
)

POSITION_COUNT_SUBQ: ScalarSelect[Any] = (
    select(func.count(position_table.c.id))
    .where(position_table.c.category_id == category_table.c.id)
    .correlate(category_table)
    .scalar_subquery()
)

ITEMS_COUNT_SUBQ: ScalarSelect[Any] = (
    select(func.count(item_table.c.id))
    .select_from(
        item_table.join(
            position_table,
            item_table.c.position_id == position_table.c.id,
        ),
    )
    .where(position_table.c.category_id == category_table.c.id)
    .correlate(category_table)
    .scalar_subquery()
)

ITEM_EXISTS_SUBQ: Select[Any] = (
    select(1)
    .select_from(
        position_table.join(
            item_table,
            item_table.c.position_id == position_table.c.id,
        ),
    )
    .where(position_table.c.category_id == category_table.c.id)
    .where(item_table.c.status == "AVAILABLE")
    .correlate(category_table)
)
