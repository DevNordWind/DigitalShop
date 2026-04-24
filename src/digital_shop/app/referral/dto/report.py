from dataclasses import dataclass

from app.common.dto.money import MoneyDTO
from domain.common.money import Currency
from frozendict import frozendict


@dataclass(slots=True, frozen=True)
class ReferrerReport:
    referral_count: int

    awards_count: int
    awards_sum: frozendict[Currency, MoneyDTO]


@dataclass(slots=True, frozen=True)
class ConvertedReferrerReport:
    report: ReferrerReport

    total: MoneyDTO
