from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.referral.entity import ReferralAward
from domain.referral.port import ReferralAwardRepository
from domain.referral.value_object import ReferralAwardId
from infra.framework.sql_alchemy.table.referral import referrer_profile_table


class ReferralAwardRepositoryImpl(ReferralAwardRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add(self, profile: ReferralAward) -> None:
        self._session.add(profile)

    async def get(self, award_id: ReferralAwardId) -> ReferralAward | None:
        stmt = select(ReferralAward).where(
            referrer_profile_table.c.id == award_id.value,
        )
        result = await self._session.scalar(stmt)

        return result or None
