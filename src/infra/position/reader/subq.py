from typing import Any

from sqlalchemy import ScalarSelect, Select, func, select

from domain.product.position.item.enums import (
    ItemStatus,
)
from infra.framework.sql_alchemy.table.position import (
    item_table,
    position_table,
)

ITEMS_COUNT_SUBQ: ScalarSelect[Any] = (
    select(func.count(item_table.c.id))
    .select_from(item_table)
    .where(item_table.c.position_id == position_table.c.id)
    .correlate(position_table)
    .scalar_subquery()
)

ITEM_EXISTS_SUBQ: Select[Any] = (
    select(1)
    .select_from(item_table)
    .where(
        item_table.c.position_id == position_table.c.id,
        item_table.c.status == ItemStatus.AVAILABLE,
    )
    .correlate(position_table)
)
