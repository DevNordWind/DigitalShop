from frozendict import frozendict

from app.app.common.dto.localized import LocalizedTextDTO
from app.domain.shopping.category.value_object import CategoryDescription


class CategoryDescriptionMapper:
    @classmethod
    def to_value_object(cls, src: LocalizedTextDTO) -> CategoryDescription:
        return CategoryDescription(
            values=frozendict(src.translations),
            default_lang=src.default_lang,
        )
