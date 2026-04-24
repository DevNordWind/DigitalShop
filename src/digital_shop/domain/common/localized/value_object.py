from dataclasses import dataclass
from typing import Self

from domain.common.localized import CannotRemoveDefaultLanguage, Language
from domain.common.localized.exception import (
    DefaultLanguageMissingError,
)
from frozendict import frozendict


@dataclass(frozen=True, slots=True)
class LocalizedText:
    values: frozendict[Language, str]
    default_lang: Language

    def __post_init__(self) -> None:
        if self.default_lang not in self.values:
            raise DefaultLanguageMissingError(lang=self.default_lang)

    def __len__(self) -> int:
        return len(self.values)

    @classmethod
    def create(cls, lang: Language, translation: str) -> Self:
        return cls(values=frozendict({lang: translation}), default_lang=lang)

    def has(self, lang: Language) -> bool:
        return lang in self.values

    def get_default(self) -> str:
        return self.values[self.default_lang]

    def set(self, lang: Language, translation: str) -> Self:
        new_values = frozendict(self.values | {lang: translation})

        return type(self)(
            values=new_values,
            default_lang=self.default_lang,
        )

    def remove(self, lang: Language) -> Self:
        if lang == self.default_lang:
            raise CannotRemoveDefaultLanguage

        return type(self)(
            values=frozendict(
                {k: v for k, v in self.values.items() if k != lang},
            ),
            default_lang=self.default_lang,
        )

    def change_default_lang(self, lang: Language) -> Self:
        return type(self)(
            values=self.values,
            default_lang=lang,
        )
