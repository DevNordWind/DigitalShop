from typing import override

from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB

from app.domain.common.file_key import FileKey, FileType


class FileKeyType(TypeDecorator[FileKey]):
    impl = JSONB
    cache_ok = True

    @override
    def process_bind_param(
        self,
        value: FileKey | None,
        dialect: Dialect,
    ) -> dict[str, str] | None:
        if value is None:
            return None

        return {"value": value.value, "type": value.type.value}

    @override
    def process_result_value(
        self,
        value: dict[str, str] | None,
        dialect: Dialect,
    ) -> FileKey | None:
        if value is None:
            return None

        return FileKey(value=value["value"], type=FileType(value["type"]))
