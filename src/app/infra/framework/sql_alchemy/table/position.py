from sqlalchemy import (
    ARRAY,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Table,
    text,
)
from sqlalchemy.ext.mutable import MutableList

from app.domain.common.localized import Language
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.enums import (
    FulfillmentType,
    PositionStatus,
    WarehouseType,
)
from app.domain.shopping.position.item.entity import FixedItem, StockItem
from app.domain.shopping.position.item.enums import FixedItemStatus, StockItemStatus

from .base import mapper_registry, metadata
from .custom_type import (
    CategoryIdType,
    FileKeyType,
    FixedItemIdType,
    ItemContentType,
    LocalizedTextType,
    PositionIdType,
    PositionPriceType,
    StockItemIdType,
    UserIdType,
)

position_table: Table = Table(
    "Position",
    metadata,
    Column(
        "id",
        PositionIdType,
        primary_key=True,
    ),
    Column(
        "category_id",
        CategoryIdType,
        ForeignKey("Category.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("creator_id", UserIdType, ForeignKey("User.id"), nullable=False),
    Column("name", LocalizedTextType, nullable=False),
    Column("description", LocalizedTextType, nullable=True),
    Column(
        "media",
        MutableList.as_mutable(ARRAY(FileKeyType())),
        nullable=False,
    ),
    Column("fulfillment_type", Enum(FulfillmentType), nullable=False),
    Column("warehouse_type", Enum(WarehouseType), nullable=False),
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


stock_item_table: Table = Table(
    "StockItem",
    metadata,
    Column("id", StockItemIdType, primary_key=True),
    Column(
        "position_id",
        PositionIdType,
        ForeignKey("Position.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("creator_id", UserIdType, ForeignKey("User.id"), nullable=False),
    Column("content", ItemContentType, nullable=False),
    Column("status", Enum(StockItemStatus), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("archived_at", DateTime(timezone=True), nullable=True),
    Column("sold_at", DateTime(timezone=True), nullable=True),
    Column("reserved_at", DateTime(timezone=True), nullable=True),
    Column("updated_at", DateTime(timezone=True), nullable=True),
)

fixed_item_table: Table = Table(
    "FixedItem",
    metadata,
    Column("id", FixedItemIdType, primary_key=True),
    Column(
        "position_id",
        PositionIdType,
        ForeignKey("Position.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    ),
    Column("creator_id", UserIdType, ForeignKey("User.id"), nullable=False),
    Column("content", ItemContentType, nullable=False),
    Column("status", Enum(FixedItemStatus), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("archived_at", DateTime(timezone=True), nullable=True),
    Column("updated_at", DateTime(timezone=True), nullable=True),
)


def map_position() -> None:
    mapper_registry.map_imperatively(
        Position,
        position_table,
    )


def map_stock_item() -> None:
    mapper_registry.map_imperatively(
        StockItem,
        stock_item_table,
    )


def map_fixed_item() -> None:
    mapper_registry.map_imperatively(
        FixedItem,
        fixed_item_table,
    )
