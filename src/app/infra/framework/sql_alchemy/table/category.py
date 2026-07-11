from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Table,
    text,
)

from app.domain.common.localized import Language
from app.domain.shopping.category.entity import Category
from app.domain.shopping.category.enums import CategoryStatus

from .base import mapper_registry, metadata
from .custom_type import CategoryIdType, FileKeyType, LocalizedTextType, UserIdType

category_table: Table = Table(
    "Category",
    metadata,
    Column("id", CategoryIdType, primary_key=True),
    Column("creator_id", UserIdType, ForeignKey("User.id"), nullable=False),
    Column("name", LocalizedTextType, nullable=False),
    Column("description", LocalizedTextType, nullable=True),
    Column("media", FileKeyType, nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
    Column("archived_at", DateTime(timezone=True), nullable=True),
    Column("status", Enum(CategoryStatus), nullable=True),
)

for lang in Language:
    Index(
        f"uq_Category_name_values_{lang.value}",
        text(f"(name->'values'->>'{lang.value}')"),
        postgresql_where=text(
            f"(name->'values'->>'{lang.value}') IS NOT NULL",
        ),
        unique=True,
        _table=category_table,
    )


def map_category() -> None:
    mapper_registry.map_imperatively(
        Category,
        category_table,
    )
