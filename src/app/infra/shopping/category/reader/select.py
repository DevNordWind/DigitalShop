from typing import Any

from sqlalchemy import Column

from app.infra.framework.sql_alchemy.table.category import category_table

CATEGORY_SELECT: tuple[Column[Any], ...] = (
    category_table.c.id,
    category_table.c.creator_id,
    category_table.c.name,
    category_table.c.description,
    category_table.c.media,
    category_table.c.created_at,
    category_table.c.updated_at,
    category_table.c.archived_at,
    category_table.c.status,
)

CATEGORY_SHORT_SELECT: tuple[Column[Any], ...] = (
    category_table.c.id,
    category_table.c.name,
    category_table.c.created_at,
    category_table.c.archived_at,
    category_table.c.status,
)
