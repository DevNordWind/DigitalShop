from operator import and_

from frozendict import frozendict
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.money import MoneyDTO
from app.common.dto.period import TimePeriod
from app.referral.dto.report import ReferrerReport
from app.referral.port import ReferralSystemReporter
from domain.referral.enums.status import ReferralAwardStatus
from domain.user.value_object import UserId
from infra.framework.sql_alchemy.table.referral import referral_award_table
from infra.framework.sql_alchemy.table.user import user_table


class ReferralSystemReporterImpl(ReferralSystemReporter):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def get_referrer_report(
        self,
        referrer_id: UserId,
        period: TimePeriod | None = None,
    ) -> ReferrerReport:
        user_filters = [user_table.c.referrer_id == referrer_id.value]
        award_filters = [
            referral_award_table.c.referrer_id == referrer_id.value,
            referral_award_table.c.status == ReferralAwardStatus.COMPLETED,
        ]

        if period:
            period_expr = and_(
                referral_award_table.c.completed_at >= period.from_date,
                referral_award_table.c.completed_at <= period.to_date,
            )
            award_filters.append(period_expr)

            user_period_expr = and_(
                user_table.c.reg_at >= period.from_date,
                user_table.c.reg_at <= period.to_date,
            )
            user_filters.append(user_period_expr)

        counts_stmt = select(
            select(func.count(user_table.c.id))
            .where(*user_filters)
            .scalar_subquery()
            .label("ref_count"),
            select(func.count(referral_award_table.c.id))
            .where(*award_filters)
            .scalar_subquery()
            .label("awards_count"),
        )

        counts_res = (await self._session.execute(counts_stmt)).first()

        awards_sum_stmt = (
            select(
                referral_award_table.c.award_currency,
                func.sum(referral_award_table.c.award_amount).label("total"),
            )
            .where(*award_filters)
            .group_by(referral_award_table.c.award_currency)
        )

        awards_sum_result = await self._session.execute(awards_sum_stmt)

        awards_sum = frozendict(
            {
                row.award_currency: MoneyDTO(
                    amount=row.total,
                    currency=row.award_currency,
                )
                for row in awards_sum_result
            },
        )

        return ReferrerReport(
            referral_count=counts_res.ref_count if counts_res else 0,
            awards_count=counts_res.awards_count if counts_res else 0,
            awards_sum=awards_sum,
        )
