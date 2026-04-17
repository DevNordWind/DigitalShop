from typing import Any

from sqlalchemy import Column

from infra.framework.sql_alchemy.table.position import (
    item_table,
    position_table,
)

POSITION_SELECT: tuple[Column[Any], ...] = (
    position_table.c.id,
    position_table.c.category_id,
    position_table.c.creator_id,
    position_table.c.name,
    position_table.c.description,
    position_table.c.warehouse,
    position_table.c.price,
    position_table.c.media,
    position_table.c.created_at,
    position_table.c.updated_at,
    position_table.c.archived_at,
    position_table.c.status,
)

POSITION_SHORT_SELECT: tuple[Column[Any], ...] = (
    position_table.c.id,
    position_table.c.category_id,
    position_table.c.creator_id,
    position_table.c.name,
    position_table.c.warehouse,
    position_table.c.price,
    position_table.c.created_at,
    position_table.c.archived_at,
    position_table.c.status,
)

ITEM_SELECT: tuple[Column[Any], ...] = (
    item_table.c.id,
    item_table.c.position_id,
    item_table.c.creator_id,
    item_table.c.content,
    item_table.c.status,
    item_table.c.created_at,
    item_table.c.updated_at,
    item_table.c.archived_at,
    item_table.c.type,
    item_table.c.sold_at,
    item_table.c.reserved_at,
)
