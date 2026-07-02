from dataclasses import dataclass

from app.app.common.dto.localized import LocalizedTextDTO
from app.domain.common.localized import Language


@dataclass(slots=True)
class CategorySettings:
    default_lang: Language
    show_with_no_items: bool

    def switch_show_with_no_items(self) -> None:
        self.show_with_no_items = not self.show_with_no_items

    def can_translate_to_others(
        self,
        localized: LocalizedTextDTO,
        current_lang: Language,
    ) -> bool:
        if (
            self.default_lang != current_lang
            or self.default_lang not in localized.translations
        ):
            return False

        return len(localized.translations) != len(Language)

    def can_use_translator(
        self,
        localized: LocalizedTextDTO,
        target_lang: Language,
    ) -> bool:
        if self.default_lang not in localized.translations:
            return False

        return target_lang != self.default_lang

    def is_default_lang_filled(self, localized: LocalizedTextDTO) -> bool:
        return self.default_lang in localized.translations
