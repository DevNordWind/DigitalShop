from app.common.dto.localized import LocalizedTextDTO
from domain.product.category.value_object import CategoryName
from frozendict import frozendict


class CategoryNameMapper:
    @classmethod
    def to_value_object(cls, src: LocalizedTextDTO) -> CategoryName:
        return CategoryName(
            values=frozendict(src.translations),
            default_lang=src.default_lang,
        )
