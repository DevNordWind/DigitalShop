from datetime import UTC, datetime
from typing import Final
from uuid import UUID

__all__ = ("FIXED_DATETIME", "FIXED_UUID")

FIXED_UUID: Final[UUID] = UUID("01a1ab14-b1da-7054-b807-50cbd3f1f148")
FIXED_DATETIME: Final[datetime] = datetime(2026, 11, 5, 9, 41, 24, 878792, tzinfo=UTC)
