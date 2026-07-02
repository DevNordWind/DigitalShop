from dataclasses import dataclass

from aiogram.enums import ContentType

from app.domain.common.file_key import FileType
from app.presentation.aiogram.exception import (
    TelegramBotError,
    TelegramBotValidationError,
)


class FileMappingError(TelegramBotError): ...


@dataclass(slots=True, frozen=True)
class UnsupportedContentTypeError(FileMappingError, TelegramBotValidationError):
    type: ContentType


class MessageNotContainFileError(FileMappingError): ...


@dataclass(slots=True, frozen=True)
class UnsupportedFileTypeError(FileMappingError, TelegramBotValidationError):
    type: FileType


@dataclass(slots=True, frozen=True)
class TelegramFileDownloadError(FileMappingError):
    file_id: str


class InvalidMediaAttachmentError(FileMappingError, TelegramBotValidationError): ...
