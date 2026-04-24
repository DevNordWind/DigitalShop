from app.common.dto.localized import LocalizedTextDTO
from domain.product.category.value_object import CategoryDescription
from frozendict import frozendict


class CategoryDescriptionMapper:
    @classmethod
    def to_value_object(cls, src: LocalizedTextDTO) -> CategoryDescription:
        return CategoryDescription(
            values=frozendict(src.translations),
            default_lang=src.default_lang,
        )
