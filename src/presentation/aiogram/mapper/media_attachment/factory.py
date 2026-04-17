from aiogram.enums import ContentType
from aiogram.types import Animation, Document, Message, PhotoSize, Video
from aiogram_dialog.api.entities import MediaAttachment, MediaId

type TelegramFile = PhotoSize | Document | Video | Animation


class MediaAttachmentFactory:
    @classmethod
    def from_message(cls, msg: Message) -> MediaAttachment:
        resolved: TelegramFile = cls._extract_tg_file(msg)

        return MediaAttachment(
            type=ContentType(msg.content_type),
            file_id=MediaId(
                file_id=resolved.file_id,
                file_unique_id=resolved.file_unique_id,
            ),
        )

    @classmethod
    def _extract_tg_file(cls, msg: Message) -> TelegramFile:
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
            case _:
                raise ValueError(
                    f"Unsupported ContentType: {msg.content_type}",
                )

        if file is None:
            raise ValueError("MessageNotContainFile")

        return file
