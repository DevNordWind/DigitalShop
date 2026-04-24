from datetime import UTC, datetime

from domain.common.port import Clock


class SystemClock(Clock):
    def now(self) -> datetime:
        return datetime.now(UTC)
