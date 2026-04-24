from dataclasses import dataclass
from uuid import UUID

from domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class ReferrerProfileDTO:
    user_id: UUID
    award_currency: Currency

    send_notifications: bool
