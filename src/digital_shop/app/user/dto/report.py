from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.user.enums import UserRole


@dataclass(slots=True, frozen=True)
class UserProfileReport:
    id: UUID
    role: UserRole

    orders_count: int
    top_ups_count: int

    reg_at: datetime
