from typing import Any

from app.app.common.dto.file_key import FileKeyMapper
from app.app.common.dto.localized import LocalizedTextMapper
from app.app.shopping.position.dto.item import FixedItemDTO, ItemDTO, StockItemDTO
from app.app.shopping.position.dto.item_content import ItemContentDTO, ItemContentMapper
from app.app.shopping.position.dto.position import PositionDTO, PositionShortDTO
from app.app.shopping.position.dto.price import PositionPriceMapper
from app.domain.shopping.position.enums import FulfillmentType


class PositionReaderMapper:
    @classmethod
    def to_dto(cls, row: Any) -> PositionDTO:
        return PositionDTO(
            id=row.id.value,
            category_id=row.category_id.value,
            creator_id=row.creator_id.value,
            name=LocalizedTextMapper.to_dto(src=row.name),
            description=(
                LocalizedTextMapper.to_dto(src=row.description)
                if row.description
                else None
            ),
            media=[FileKeyMapper.to_dto(src=key) for key in row.media],
            price=PositionPriceMapper.to_dto(row.price),
            warehouse_type=row.warehouse_type,
            created_at=row.created_at,
            updated_at=row.updated_at,
            archived_at=row.archived_at,
            status=row.status,
            fulfillment_type=row.fulfillment_type,
        )

    @classmethod
    def to_short_dto(cls, row: Any) -> PositionShortDTO:
        return PositionShortDTO(
            id=row.id.value,
            category_id=row.category_id.value,
            creator_id=row.creator_id.value,
            name=LocalizedTextMapper.to_dto(src=row.name),
            price=PositionPriceMapper.to_dto(src=row.price),
            warehouse_type=row.warehouse_type,
            created_at=row.created_at,
            archived_at=row.archived_at,
            status=row.status,
            fulfillment_type=row.fulfillment_type,
        )

    @classmethod
    def to_item_dto(cls, row: Any, fulfillment_type: FulfillmentType) -> ItemDTO:
        match fulfillment_type:
            case FulfillmentType.STOCK:
                return cls.to_stock_item_dto(row=row)
            case FulfillmentType.FIXED:
                return cls.to_fixed_item_dto(row=row)

    @classmethod
    def to_stock_item_dto(cls, row: Any) -> StockItemDTO:
        return StockItemDTO(
            id=row.id.value,
            position_id=row.position_id.value,
            creator_id=row.creator_id.value,
            content=ItemContentDTO(row.content.value),
            status=row.status,
            sold_at=row.sold_at,
            reserved_at=row.reserved_at,
            created_at=row.created_at,
            archived_at=row.archived_at,
            updated_at=row.updated_at,
        )

    @classmethod
    def to_fixed_item_dto(cls, row: Any) -> FixedItemDTO:
        return FixedItemDTO(
            id=row.id.value,
            position_id=row.position_id.value,
            creator_id=row.creator_id.value,
            content=ItemContentMapper.to_dto(src=row.content),
            status=row.status,
            created_at=row.created_at,
            archived_at=row.archived_at,
            updated_at=row.updated_at,
        )
