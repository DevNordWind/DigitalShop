from dataclasses import dataclass

from domain.common.localized import Language


@dataclass(slots=True, frozen=True)
class I18nText:
    key: str


@dataclass(slots=True, frozen=True)
class LocalizedText:
    texts: dict[Language, str]


type BroadcastText = I18nText | LocalizedText
