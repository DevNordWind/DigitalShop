from typing import Any

from app.common.dto.file_key import FileKeyMapper
from app.common.dto.localized import LocalizedTextMapper
from app.product.category.dto.category import CategoryDTO, CategoryShortDTO


class CategoryReaderMapper:
    @classmethod
    def to_dto(cls, row: Any) -> CategoryDTO:
        return CategoryDTO(
            id=row.id,
            creator_id=row.creator_id,
            name=LocalizedTextMapper.to_dto(src=row.name),
            description=LocalizedTextMapper.to_dto(src=row.description)
            if row.description
            else None,
            media=FileKeyMapper.to_dto(src=row.media) if row.media else None,
            created_at=row.created_at,
            updated_at=row.updated_at,
            archived_at=row.archived_at,
            status=row.status,
        )

    @classmethod
    def to_short_dto(cls, row: Any) -> CategoryShortDTO:
        return CategoryShortDTO(
            id=row.id,
            name=LocalizedTextMapper.to_dto(src=row.name),
            created_at=row.created_at,
            status=row.status,
            archived_at=row.archived_at,
        )
