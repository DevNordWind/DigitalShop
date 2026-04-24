from dataclasses import dataclass
from typing import Final
from uuid import UUID

CTX_KEY: Final[str] = "CTX"

ARCHIVED_ITEMS_SCROLL_ID: Final[str] = "ARCHIVED_ITEMS_SCROLL_ID"
ARCHIVED_ITEMS_SCROLL_HEIGHT: Final[int] = 8


@dataclass(slots=True)
class PositionFixedItemCtx:
    position_id: UUID
    current_item_id: UUID | None = None

    current_archived_item_id: UUID | None = None
