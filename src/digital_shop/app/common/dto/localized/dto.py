from dataclasses import dataclass

from domain.common.localized import Language


@dataclass(slots=True, frozen=True)
class LocalizedTextDTO:
    default_lang: Language
    translations: dict[Language, str]

    def get(self, lang: Language) -> str | None:
        return self.translations.get(lang)

    def get_with_fallback(self, lang: Language | None) -> str:
        if lang is None:
            return self.translations[self.default_lang]

        translation: str | None = self.translations.get(lang)
        if translation is None:
            return self.translations[self.default_lang]

        return translation
