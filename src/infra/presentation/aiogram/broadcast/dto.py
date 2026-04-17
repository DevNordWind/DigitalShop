from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class MessageResult(StrEnum):
    SUCCESS = "SUCCESS"
    NOT_ACTIVE = "NOT_ACTIVE"
    ERROR = "ERROR"


@dataclass(slots=True, frozen=True)
class BroadcastProgress:
    id: UUID

    success: int
    error: int
    not_active: int
    total: int

    current_message_id: int | None

    @property
    def current(self) -> int:
        return self.success + self.error + self.not_active
