from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.user.enums import UserRole


@dataclass(slots=True, frozen=True)
class UserProfileDTO:
    id: UUID
    role: UserRole

    orders_count: int
    top_ups_count: int

    reg_at: datetime
