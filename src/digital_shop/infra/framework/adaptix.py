from pathlib import Path
from typing import Any, TypedDict

from adaptix import Provider, dumper, loader
from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from domain.common.exchange_rate import CurrencyPair
from domain.common.money import Currency


class MediaIdDict(TypedDict):
    file_id: str
    file_unique_id: str | None


type MediaAttachmentDict = dict[str, Any]


def _serialize_media_id(media_id: MediaId | None) -> MediaIdDict | None:
    if media_id is None:
        return None
    return MediaIdDict(
        file_id=media_id.file_id,
        file_unique_id=media_id.file_unique_id,
    )


def _deserialize_media_id(data: MediaIdDict | None) -> MediaId | None:
    if data is None:
        return None

    return MediaId(
        file_id=data["file_id"],
        file_unique_id=data["file_unique_id"],
    )


def _serialize_media_attachment(m: MediaAttachment) -> MediaAttachmentDict:
    return {
        "type": m.type.value if isinstance(m.type, ContentType) else m.type,
        "url": m.url,
        "path": str(m.path) if m.path is not None else None,
        "file_id": _serialize_media_id(m.file_id),
        "use_pipe": m.use_pipe,
        "kwargs": m.kwargs,
    }


def _deserialize_media_attachment(d: MediaAttachmentDict) -> MediaAttachment:
    kwargs: dict[str, Any] = d.get("kwargs") or {}
    return MediaAttachment(
        type=ContentType(d["type"]),
        url=d.get("url"),
        path=Path(d["path"]) if d.get("path") else None,
        file_id=_deserialize_media_id(d.get("file_id")),
        use_pipe=d.get("use_pipe", False),
        **kwargs,
    )


def get_media_attachment_recipe() -> list[Provider]:
    return [
        dumper(MediaId, _serialize_media_id),
        loader(MediaId, _deserialize_media_id),
        dumper(MediaAttachment, _serialize_media_attachment),
        loader(MediaAttachment, _deserialize_media_attachment),
    ]


def deserialize_pair(pair: str) -> CurrencyPair:
    split = pair.split(":")

    return CurrencyPair(
        source=Currency(split[0]),
        target=Currency(split[1]),
    )


def get_exchange_rate_recipe() -> list[Provider]:
    return [
        dumper(CurrencyPair, lambda pair: f"{pair.source}:{pair.target}"),
        loader(CurrencyPair, deserialize_pair),
    ]
