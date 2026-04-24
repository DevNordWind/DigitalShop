from typing import Any

from app.common.dto.file_key import FileKeyMapper
from app.common.dto.localized import LocalizedTextMapper
from app.product.position.dto.item import (
    FiniteItemDTO,
    InfiniteItemDTO,
    ItemDTO,
)
from app.product.position.dto.item_content import ItemContentMapper
from app.product.position.dto.position import PositionDTO, PositionShortDTO
from app.product.position.dto.price import PositionPriceMapper
from infra.framework.sql_alchemy.table.position import ItemType


class PositionReaderMapper:
    @classmethod
    def to_dto(cls, row: Any) -> PositionDTO:
        return PositionDTO(
            id=row.id,
            category_id=row.category_id,
            creator_id=row.creator_id,
            name=LocalizedTextMapper.to_dto(src=row.name),
            description=LocalizedTextMapper.to_dto(src=row.description)
            if row.description
            else None,
            media=[FileKeyMapper.to_dto(src=key) for key in row.media],
            price=PositionPriceMapper.to_dto(row.price),
            warehouse_type=row.warehouse.type,
            created_at=row.created_at,
            updated_at=row.updated_at,
            archived_at=row.archived_at,
            status=row.status,
        )

    @classmethod
    def to_short_dto(cls, row: Any) -> PositionShortDTO:
        return PositionShortDTO(
            id=row.id,
            category_id=row.category_id,
            creator_id=row.creator_id,
            name=LocalizedTextMapper.to_dto(src=row.name),
            price=PositionPriceMapper.to_dto(src=row.price),
            warehouse_type=row.warehouse.type,
            created_at=row.created_at,
            archived_at=row.archived_at,
            status=row.status,
        )

    @classmethod
    def to_item_dto(cls, row: Any) -> ItemDTO:
        match row.type:
            case ItemType.FINITE:
                return cls._to_finite_item_dto(row)
            case ItemType.INFINITE:
                return cls._to_infinite_item_dto(row)
            case _:
                raise ValueError(f"Unknown ItemType: {row.type}")

    @classmethod
    def _to_finite_item_dto(cls, row: Any) -> FiniteItemDTO:
        return FiniteItemDTO(
            id=row.id,
            position_id=row.position_id,
            creator_id=row.creator_id,
            content=ItemContentMapper.to_dto(src=row.content),
            status=row.status,
            sold_at=row.sold_at,
            reserved_at=row.reserved_at,
            created_at=row.created_at,
            archived_at=row.archived_at,
            updated_at=row.updated_at,
        )

    @classmethod
    def _to_infinite_item_dto(cls, row: Any) -> InfiniteItemDTO:
        return InfiniteItemDTO(
            id=row.id,
            position_id=row.position_id,
            creator_id=row.creator_id,
            content=ItemContentMapper.to_dto(src=row.content),
            status=row.status,
            created_at=row.created_at,
            archived_at=row.archived_at,
            updated_at=row.updated_at,
        )
