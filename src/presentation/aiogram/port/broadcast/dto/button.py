from dataclasses import dataclass

from presentation.aiogram.port.broadcast.dto.text import (
    BroadcastText,
    LocalizedText,
)


@dataclass(slots=True, frozen=True)
class BroadcastButton:
    text: BroadcastText


@dataclass(slots=True, frozen=True)
class UrlButton(BroadcastButton):
    text: LocalizedText

    url: str


@dataclass(slots=True, frozen=True)
class DataButton(BroadcastButton):
    text: BroadcastText
    data: str
