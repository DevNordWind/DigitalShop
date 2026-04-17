from dataclasses import dataclass

from domain.common.file import (
    FileKeyInvalidFormatError,
    FileKeyTooLongError,
    FileType,
)
from domain.common.file.const import FILE_KEY_MAX_LENGTH, FILE_KEY_PATTERN


@dataclass(frozen=True, slots=True)
class FileKey:
    value: str
    type: FileType

    def __post_init__(self) -> None:
        raw = self.value.strip()

        if len(raw) > FILE_KEY_MAX_LENGTH:
            raise FileKeyTooLongError(FILE_KEY_MAX_LENGTH)

        if raw.startswith("/") or raw.endswith("/"):
            raise FileKeyInvalidFormatError(
                "Leading/trailing slash is not allowed",
            )

        if "//" in raw or ".." in raw:
            raise FileKeyInvalidFormatError("Invalid path sequence")

        normalized = raw.lower()

        if not FILE_KEY_PATTERN.fullmatch(normalized):
            raise FileKeyInvalidFormatError("Invalid media key format")

        object.__setattr__(self, "value", normalized)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FileKey):
            return False

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    @property
    def is_media(self) -> bool:
        return self.type in (
            FileType.GIF,
            FileType.PHOTO,
            FileType.VIDEO,
        )

    @property
    def is_document(self) -> bool:
        return self.type == FileType.DOCUMENT


@dataclass(slots=True, frozen=True)
class FileKeyRaw:
    type: FileType
    extension: str | None
