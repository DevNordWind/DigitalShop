from typing import Any

from sqlalchemy import Column

from app.infra.framework.sql_alchemy.table.position import (
    fixed_item_table,
    position_table,
    stock_item_table,
)

POSITION_SELECT: tuple[Column[Any], ...] = (
    position_table.c.id,
    position_table.c.category_id,
    position_table.c.creator_id,
    position_table.c.name,
    position_table.c.description,
    position_table.c.warehouse_type,
    position_table.c.fulfillment_type,
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
    position_table.c.warehouse_type,
    position_table.c.fulfillment_type,
    position_table.c.price,
    position_table.c.created_at,
    position_table.c.archived_at,
    position_table.c.status,
)

FIXED_ITEM_SELECT: tuple[Column[Any], ...] = (
    fixed_item_table.c.id,
    fixed_item_table.c.position_id,
    fixed_item_table.c.creator_id,
    fixed_item_table.c.content,
    fixed_item_table.c.status,
    fixed_item_table.c.created_at,
    fixed_item_table.c.updated_at,
    fixed_item_table.c.archived_at,
)

STOCK_ITEM_SELECT: tuple[Column[Any], ...] = (
    stock_item_table.c.id,
    stock_item_table.c.position_id,
    stock_item_table.c.creator_id,
    stock_item_table.c.content,
    stock_item_table.c.status,
    stock_item_table.c.created_at,
    stock_item_table.c.updated_at,
    stock_item_table.c.archived_at,
    stock_item_table.c.sold_at,
    stock_item_table.c.reserved_at,
)
