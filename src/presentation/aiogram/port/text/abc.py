from abc import ABC, abstractmethod
from typing import Any

from domain.common.localized import Language


class Text(ABC):
    @abstractmethod
    def __call__(self, key: str, **kwargs: Any) -> str:
        raise NotImplementedError

    def key_exists(self, key: str) -> bool:
        raise NotImplementedError


class TranslatorHub(ABC):
    @abstractmethod
    def __call__(self, lang: Language | None = None) -> Text:
        raise NotImplementedError
