from collections.abc import AsyncIterator
from pathlib import Path
from typing import BinaryIO, Final

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import Animation, Document, File, Message, PhotoSize, Video
from aiogram_dialog.api.entities import MediaAttachment

from app.common.dto.file_key import FileKeyRawDTO
from domain.common.file import FileType
from presentation.aiogram.mapper.file.exception import (
    InvalidMediaAttachment,
    MessageNotContainFile,
    TelegramFileDownloadError,
    UnsupportedContentType,
)
from presentation.aiogram.mapper.file.mapper import FileTypeMapper

type TelegramFile = PhotoSize | Document | Video | Animation

_CHUNK_SIZE: Final[int] = 1024 * 1024


class FileDTOFactory:
    def __init__(self, bot: Bot) -> None:
        self._bot: Bot = bot

    async def from_message(self, msg: Message) -> FileKeyRawDTO:
        file_type: FileType = FileTypeMapper.to_domain(
            src=ContentType(msg.content_type),
        )
        tg_file: TelegramFile = self._extract_tg_file(msg)
        resolved: File = await self._resolve_file(tg_file.file_id)

        return FileKeyRawDTO(
            type=file_type,
            extension=self._extract_extension(resolved.file_path),
            content=self._stream_file(resolved),
        )

    async def from_media_attachment(
        self,
        attachment: MediaAttachment,
    ) -> FileKeyRawDTO:
        file_type: FileType = FileTypeMapper.to_domain(src=attachment.type)
        if not attachment.file_id or not attachment.file_id.file_id:
            raise InvalidMediaAttachment

        resolved: File = await self._resolve_file(attachment.file_id.file_id)

        return FileKeyRawDTO(
            type=file_type,
            extension=self._extract_extension(resolved.file_path),
            content=self._stream_file(resolved),
        )

    @staticmethod
    def _extract_extension_from_attachment(
        attachment: MediaAttachment,
    ) -> str | None:
        if attachment.path is not None:
            suffix = Path(attachment.path).suffix
            return suffix or None
        return None

    def _extract_tg_file(self, msg: Message) -> TelegramFile:
        file: TelegramFile | None = None

        match msg.content_type:
            case ContentType.PHOTO:
                file = msg.photo[-1] if msg.photo else None
            case ContentType.DOCUMENT:
                file = msg.document
            case ContentType.ANIMATION:
                file = msg.animation
            case ContentType.VIDEO:
                file = msg.video
            case ContentType.DOCUMENT:
                file = msg.document
            case _:
                raise UnsupportedContentType(ContentType(msg.content_type))

        if file is None:
            raise MessageNotContainFile

        return file

    async def _resolve_file(self, file_id: str) -> File:
        file: File = await self._bot.get_file(file_id)
        if file.file_path is None:
            raise TelegramFileDownloadError(file_id)
        return file

    async def _stream_file(self, file: File) -> AsyncIterator[bytes]:
        if not file.file_path:
            raise TelegramFileDownloadError(file.file_id)

        stream: BinaryIO | None = await self._bot.download_file(file.file_path)

        if stream is None:
            raise TelegramFileDownloadError(file.file_id)

        while chunk := stream.read(_CHUNK_SIZE):
            yield chunk

    @staticmethod
    def _extract_extension(file_path: str | None) -> str | None:
        if file_path is None:
            return None
        suffix = Path(file_path).suffix
        return suffix or None
