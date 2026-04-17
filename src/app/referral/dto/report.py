from dataclasses import dataclass

from frozendict import frozendict

from app.common.dto.money import MoneyDTO
from domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class ReferrerReport:
    referral_count: int

    awards_count: int
    awards_sum: frozendict[Currency, MoneyDTO]


@dataclass(slots=True, frozen=True)
class ConvertedReferrerReport:
    report: ReferrerReport

    total: MoneyDTO
