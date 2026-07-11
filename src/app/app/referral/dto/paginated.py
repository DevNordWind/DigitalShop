from dataclasses import dataclass

from app.app.referral.dto.award import ReferralAwardDTO


@dataclass(slots=True, frozen=True)
class ReferralAwardsPaginated:
    awards: list[ReferralAwardDTO]
    total: int
