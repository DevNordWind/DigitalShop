import logging

from googletrans import (  # type: ignore[import-untyped]
    Translator as GoogleTranslator,
)
from googletrans.models import Translated  # type: ignore[import-untyped]

from app.common.port import Translator
from app.common.port.translator import TranslatorError
from domain.common.localized import Language

logger = logging.getLogger(__name__)


class UnofficialGoogleTranslator(Translator):
    def __init__(self, translator: GoogleTranslator):
        self._translator: GoogleTranslator = translator

    async def translate(
        self,
        source: Language,
        target: Language,
        text: str,
    ) -> str:
        if source == target:
            return text

        try:
            translated: Translated = await self._translator.translate(
                text=text,
                src=source.value,
                dest=target.value,
            )
        except Exception as e:
            logger.error("UnofficialGoogleTranslator: %s", e)
            raise TranslatorError from e

        return translated.text  # type: ignore[no-any-return]
