from datetime import UTC, datetime
from typing import override

from app.domain.common.port import Clock


class SystemClock(Clock):
    @override
    def now(self) -> datetime:
        return datetime.now(UTC)
