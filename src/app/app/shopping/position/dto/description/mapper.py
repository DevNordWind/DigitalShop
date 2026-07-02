from frozendict import frozendict

from app.app.common.dto.localized import LocalizedTextDTO
from app.domain.shopping.position.value_object import PositionDescription


class PositionDescriptionMapper:
    @classmethod
    def to_value_object(cls, src: LocalizedTextDTO) -> PositionDescription:
        return PositionDescription(
            values=frozendict(src.translations),
            default_lang=src.default_lang,
        )
