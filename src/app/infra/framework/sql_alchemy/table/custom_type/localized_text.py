from typing import Any, override

from frozendict import frozendict
from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB

from app.domain.common.localized import Language, LocalizedText


class LocalizedTextType(TypeDecorator[LocalizedText]):
    impl = JSONB
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: LocalizedText | None,
        dialect: Dialect,
    ) -> dict[str, Any] | None:
        if value is None:
            return None

        return {
            "default_lang": value.default_lang.value,
            "values": {lang.value: text for lang, text in value.values.items()},
        }

    @override
    def process_result_value(
        self,
        value: dict[str, Any] | None,
        dialect: Dialect,
    ) -> LocalizedText | None:
        if value is None:
            return None

        return LocalizedText(
            values=frozendict(
                {Language(lang): text for lang, text in value["values"].items()},
            ),
            default_lang=Language(value=value["default_lang"]),
        )
