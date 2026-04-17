from frozendict import frozendict

from app.common.dto.localized import LocalizedTextDTO
from domain.product.position.value_object import PositionName


class PositionNameMapper:
    @classmethod
    def to_value_object(cls, src: LocalizedTextDTO) -> PositionName:
        return PositionName(
            values=frozendict(src.translations),
            default_lang=src.default_lang,
        )
