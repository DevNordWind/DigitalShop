from app.common.dto.localized import LocalizedTextDTO
from domain.product.position.value_object import PositionDescription
from frozendict import frozendict


class PositionDescriptionMapper:
    @classmethod
    def to_value_object(cls, src: LocalizedTextDTO) -> PositionDescription:
        return PositionDescription(
            values=frozendict(src.translations),
            default_lang=src.default_lang,
        )
