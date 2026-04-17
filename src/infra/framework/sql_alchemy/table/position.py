from enum import StrEnum

from sqlalchemy import (
    ARRAY,
    UUID,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Table,
    text,
)
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Composite, column_property, composite

from domain.common.localized import Language
from domain.product.category.value_object import CategoryId
from domain.product.position.entity import Position
from domain.product.position.enums import PositionStatus
from domain.product.position.item.entity import FiniteItem, InfiniteItem, Item
from domain.product.position.item.enums import ItemStatus
from domain.product.position.item.value_object import ItemId
from domain.product.position.value_object import PositionId
from domain.user.value_object import UserId

from .base import mapper_registry, metadata
from .custom_type import (
    FileKeyType,
    ItemContentType,
    LocalizedTextType,
    PositionPriceType,
    WarehouseStrategyType,
)


class ItemType(StrEnum):
    FINITE = "FINITE"
    INFINITE = "INFINITE"


position_table: Table = Table(
    "Position",
    metadata,
    Column(
        "id",
        UUID,
        primary_key=True,
    ),
    Column(
        "category_id",
        ForeignKey("Category.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("creator_id", ForeignKey("User.id"), nullable=False),
    Column("name", LocalizedTextType, nullable=False),
    Column("description", LocalizedTextType, nullable=True),
    Column(
        "media",
        MutableList.as_mutable(ARRAY(FileKeyType())),
        nullable=False,
    ),
    Column("warehouse", WarehouseStrategyType, nullable=False),
    Column("price", PositionPriceType, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
    Column("archived_at", DateTime(timezone=True), nullable=True),
    Column("status", Enum(PositionStatus), nullable=False),
)

for lang in Language:
    Index(
        f"uq_Position_name_values_{lang.value}",
        text(f"(name->'values'->>'{lang.value}')"),
        postgresql_where=text(
            f"(name->'values'->>'{lang.value}') IS NOT NULL",
        ),
        unique=True,
        _table=position_table,
    )

item_table: Table = Table(
    "Item",
    metadata,
    Column("id", UUID, primary_key=True),
    Column(
        "position_id",
        ForeignKey("Position.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("creator_id", ForeignKey("User.id"), nullable=False),
    Column("content", ItemContentType(), nullable=False),
    Column("status", Enum(ItemStatus), nullable=False),
    Column("type", Enum(ItemType), nullable=False),
    Column("archived_at", DateTime(timezone=True), nullable=True),
    Column("sold_at", DateTime(timezone=True), nullable=True),
    Column("reserved_at", DateTime(timezone=True), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
)


def map_position() -> None:
    mapper_registry.map_imperatively(
        Position,
        position_table,
        properties={
            "id": Composite(PositionId, position_table.c.id),
            "_id": position_table.c.id,
            "category_id": Composite(CategoryId, position_table.c.category_id),
            "_category_id": position_table.c.category_id,
            "creator_id": Composite(UserId, position_table.c.creator_id),
            "_creator_id": position_table.c.creator_id,
        },
    )


def map_item() -> None:
    mapper_registry.map_imperatively(
        Item,  # type: ignore[type-abstract]
        item_table,
        polymorphic_on=item_table.c.type,
        properties={
            "id": composite(ItemId, item_table.c.id),
            "_id": item_table.c.id,
            "position_id": composite(PositionId, item_table.c.position_id),
            "_position_id": item_table.c.position_id,
            "creator_id": composite(UserId, item_table.c.creator_id),
            "_creator_id": item_table.c.creator_id,
        },
    )
    mapper_registry.map_imperatively(
        FiniteItem,
        item_table,
        inherits=Item,
        polymorphic_identity=ItemType.FINITE,
        properties={
            "type": column_property(
                item_table.c.type,
                init=False,
                default=ItemType.FINITE,
            ),
        },
    )
    mapper_registry.map_imperatively(
        InfiniteItem,
        item_table,
        inherits=Item,
        polymorphic_identity=ItemType.INFINITE,
        properties={
            "type": column_property(
                item_table.c.type,
                init=False,
                default=ItemType.INFINITE,
            ),
        },
    )
