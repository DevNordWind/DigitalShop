from frozendict import frozendict

from app.common.dto.localized import LocalizedTextDTO
from domain.common.localized import LocalizedText


class LocalizedTextMapper:
    @classmethod
    def to_value_object(cls, src: LocalizedTextDTO) -> LocalizedText:
        return LocalizedText(
            default_lang=src.default_lang,
            values=frozendict(src.translations),
        )

    @classmethod
    def to_dto(cls, src: LocalizedText) -> LocalizedTextDTO:
        return LocalizedTextDTO(
            default_lang=src.default_lang,
            translations=dict(src.values),
        )
