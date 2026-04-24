from typing import Any

from infra.framework.sql_alchemy.table.referral import referral_award_table
from sqlalchemy import Column

REFERRAL_AWARD_SELECT: tuple[Column[Any], ...] = (
    referral_award_table.c.id,
    referral_award_table.c.referrer_id,
    referral_award_table.c.status,
    referral_award_table.c.source_reference_id,
    referral_award_table.c.source_type,
    referral_award_table.c.source_amount,
    referral_award_table.c.source_currency,
    referral_award_table.c.coefficient_snapshot,
    referral_award_table.c.award_amount,
    referral_award_table.c.award_currency,
    referral_award_table.c.exchange_rate_snapshot,
    referral_award_table.c.completed_at,
    referral_award_table.c.created_at,
)
