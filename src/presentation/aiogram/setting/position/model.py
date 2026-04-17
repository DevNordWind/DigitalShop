from dataclasses import dataclass

from app.common.dto.localized import LocalizedTextDTO
from app.product.position.dto.price import PositionPriceDTO
from domain.common.localized import Language
from domain.common.money import Currency


@dataclass(slots=True)
class PositionSettings:
    default_lang: Language
    default_currency: Currency

    show_with_no_items: bool

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

    def can_convert_to_others(
        self,
        price: PositionPriceDTO,
        current_currency: Currency,
    ) -> bool:
        return not (
            self.default_currency != current_currency
            or self.default_currency not in price.prices
        )

    def is_default_lang_filled(self, localized: LocalizedTextDTO) -> bool:
        return self.default_lang in localized.translations
