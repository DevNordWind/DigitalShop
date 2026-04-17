import logging
from pathlib import Path
from typing import Any
from uuid import UUID

from fluent_compiler.bundle import FluentBundle  # type: ignore[import-untyped]

from domain.common.localized import Language
from presentation.aiogram.port import Text, TranslatorHub

NeedStringify = None | bool | UUID

logger = logging.getLogger(__name__)


class FluentText(Text):
    def __init__(self, bundle: FluentBundle, fallback_bundle: FluentBundle):
        self.bundle: FluentBundle = bundle
        self.fallback_bundle: FluentBundle = fallback_bundle

    def __call__(self, key: str, **kwargs: Any) -> str:
        processed: dict[str, str] = (
            self._handle_kwargs(kwargs) if kwargs else {}
        )
        try:
            result, errors = self.bundle.format(key, processed)
        except KeyError:
            try:
                result, errors = self.fallback_bundle.format(key, processed)
            except KeyError:
                logger.error(
                    f"{self.__class__.__name__}: Key '{key}' not found",
                )
                return key
        if errors:
            logger.error(errors)
        return result  # type: ignore[no-any-return]

    def key_exists(self, key: str) -> bool:
        return key in self.bundle._compiled_messages  # noqa: SLF001

    @staticmethod
    def _handle_kwargs(kwargs: dict[str, Any]) -> dict[str, str]:
        return {
            k: str(v) if isinstance(v, NeedStringify) else v
            for k, v in kwargs.items()
        }


class FluentTranslatorHub(TranslatorHub):
    def __init__(
        self,
        base_dir: Path = Path("./texts"),
        default_lang: Language = Language.RU,
    ):
        self.base_dir: Path = base_dir
        self.default_lang: Language = default_lang
        self.bundles: dict[Language, FluentBundle] = {
            Language.RU: FluentBundle.from_files(
                locale="ru-RU",
                filenames=self.get_files(Language.RU),
                use_isolating=False,
            ),
            Language.EN: FluentBundle.from_files(
                locale="en-US",
                filenames=self.get_files(Language.EN),
                use_isolating=False,
            ),
        }

    def __call__(self, lang: Language | None = None) -> FluentText:
        if lang is None:
            return FluentText(
                bundle=self.bundles[self.default_lang],
                fallback_bundle=self.bundles[self.default_lang],
            )

        return FluentText(
            bundle=self.bundles[lang],
            fallback_bundle=self.bundles[self.default_lang],
        )

    def get_files(self, locale_dir: str | None = None) -> list[Path]:
        path = self.base_dir / locale_dir if locale_dir else self.base_dir

        if not path.exists():
            return []

        return list(path.rglob("*.ftl"))
