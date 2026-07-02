from frozendict import frozendict

from app.app.common.dto.localized import LocalizedTextDTO
from app.domain.shopping.category.value_object import CategoryName


class CategoryNameMapper:
    @classmethod
    def to_value_object(cls, src: LocalizedTextDTO) -> CategoryName:
        return CategoryName(
            values=frozendict(src.translations),
            default_lang=src.default_lang,
        )
