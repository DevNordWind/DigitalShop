from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Final
from uuid import UUID

from app.common.dto.query_params import SortingOrder

CTX_KEY: Final[str] = "CTX"

AWARDS_SCROLL: Final[str] = "AWARDS_SCROLL"
AWARDS_HEIGHT: Final[int] = 8


class TimeUnit(StrEnum):
    TODAY = "TODAY"
    WEEK = "WEEK"
    MONTH = "MONTH"

    def calculate_from(self, now: datetime) -> datetime:
        return {
            TimeUnit.TODAY: datetime.now(tz=UTC).replace(
                hour=0,
                minute=0,
                second=0,
            ),
            TimeUnit.MONTH: now - timedelta(days=30),
            TimeUnit.WEEK: now - timedelta(days=7),
        }[self]


@dataclass(slots=True, kw_only=True)
class ReferralCtx:
    current_time_unit: TimeUnit | None = None
    current_sorting_order: SortingOrder

    current_award_id: UUID | None = None
