from dataclasses import dataclass, field
from enum import Enum


@dataclass(slots=True, frozen=True)
class Button:
    key: str
    data: str


DEFAULT_BUTTON: Button = Button(key="inl-ui.close", data="service:close")


@dataclass(frozen=True, slots=True)
class NotificationRequest:
    key: str
    buttons: list[Button] = field(default_factory=lambda: [DEFAULT_BUTTON])


class MessageResult(Enum):
    SUCCESS = 0
    ERROR = 1
    NOT_ACTIVE = 2
