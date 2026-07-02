from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Self

from frozendict import frozendict

from app.domain.common.localized.enums import Language
from app.domain.common.localized.exception import (
    DefaultLanguageDeletionForbiddenError,
    DefaultLanguageMissingError,
)


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

    @property
    def default(self) -> str:
        return self.values[self.default_lang]

    def has(self, lang: Language) -> bool:
        return lang in self.values

    def set(self, lang: Language, translation: str) -> Self:
        new_values = MappingProxyType(self.values | {lang: translation})

        return replace(
            self,
            values=new_values,
            default_lang=self.default_lang,
        )

    def remove(self, lang: Language) -> Self:
        if lang == self.default_lang:
            raise DefaultLanguageDeletionForbiddenError

        return replace(
            self,
            values=MappingProxyType(
                {k: v for k, v in self.values.items() if k != lang},
            ),
            default_lang=self.default_lang,
        )

    def change_default_lang(self, lang: Language) -> Self:
        return replace(
            self,
            values=self.values,
            default_lang=lang,
        )
