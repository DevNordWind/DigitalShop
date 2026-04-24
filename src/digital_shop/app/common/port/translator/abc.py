from abc import ABC, abstractmethod

from domain.common.localized import Language


class Translator(ABC):
    @abstractmethod
    async def translate(
        self,
        source: Language,
        target: Language,
        text: str,
    ) -> str:
        raise NotImplementedError
