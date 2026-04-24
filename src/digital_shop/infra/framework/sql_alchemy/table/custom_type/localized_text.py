from functools import lru_cache

from domain.common.localized import Language, LocalizedText
from frozendict import frozendict
from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB

type LocalizedTextDict = dict[str, str | dict[str, str]]


@lru_cache(maxsize=128)
def _parse_language(value: str) -> Language:
    return Language(value)


class LocalizedTextType(TypeDecorator[LocalizedText]):
    impl = JSONB
    cache_ok = True

    def process_bind_param(
        self,
        value: LocalizedText | None,
        dialect: Dialect,
    ) -> LocalizedTextDict | None:
        if value is None:
            return None

        return {
            "default_lang": value.default_lang.value,
            "values": {
                lang.value: text for lang, text in value.values.items()
            },
        }

    def process_result_value(
        self,
        value: LocalizedTextDict | None,
        dialect: Dialect,
    ) -> LocalizedText | None:
        if value is None:
            return None

        return LocalizedText(
            values=frozendict(
                {
                    Language(lang): text
                    for lang, text in value["values"].items()  # type: ignore[union-attr]
                },
            ),
            default_lang=_parse_language(value=value["default_lang"]),  # type: ignore[arg-type]
        )
