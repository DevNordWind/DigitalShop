from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Table,
    text,
)
from sqlalchemy.orm import Composite

from domain.common.localized import Language
from domain.product.category.entity import Category
from domain.product.category.enums import CategoryStatus
from domain.product.category.value_object import CategoryId
from domain.user.value_object import UserId

from .base import mapper_registry, metadata
from .custom_type import FileKeyType, LocalizedTextType

category_table: Table = Table(
    "Category",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("creator_id", ForeignKey("User.id"), nullable=False),
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
        properties={
            "id": Composite(CategoryId, category_table.c.id),
            "creator_id": Composite(UserId, category_table.c.creator_id),
            "_id": category_table.c.id,
            "_creator_id": category_table.c.creator_id,
        },
    )
