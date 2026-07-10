from typing import Any

from app.app.shopping.position.dto.item import FixedItemDTO, StockItemDTO
from app.app.shopping.position.dto.item_content import ItemContentDTO, ItemContentMapper


class PositionItemMapper:
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
