from typing import Any

from app.app.common.dto.file_key import FileKeyMapper
from app.app.common.dto.localized import LocalizedTextMapper
from app.app.shopping.category.dto.category import (
    CategoryDTO,
    CategoryShortDTO,
    CategoryWithGoodsAmountDTO,
)


class CategoryReaderMapper:
    @classmethod
    def to_dto(cls, row: Any) -> CategoryDTO:
        return CategoryDTO(
            id=row.id.value,
            creator_id=row.creator_id.value,
            name=LocalizedTextMapper.to_dto(src=row.name),
            description=(
                LocalizedTextMapper.to_dto(src=row.description)
                if row.description
                else None
            ),
            media=FileKeyMapper.to_dto(src=row.media) if row.media else None,
            created_at=row.created_at,
            updated_at=row.updated_at,
            archived_at=row.archived_at,
            status=row.status,
        )

    @classmethod
    def to_short_dto(cls, row: Any) -> CategoryShortDTO:
        return CategoryShortDTO(
            id=row.id.value,
            name=LocalizedTextMapper.to_dto(src=row.name),
            created_at=row.created_at,
            archived_at=row.archived_at,
            status=row.status,
        )

    @classmethod
    def to_with_goods_amount_dto(cls, row: Any) -> CategoryWithGoodsAmountDTO:
        return CategoryWithGoodsAmountDTO(
            category=cls.to_dto(row=row),
            positions_amount=row.positions_amount,
            items_amount=row.items_amount,
        )
