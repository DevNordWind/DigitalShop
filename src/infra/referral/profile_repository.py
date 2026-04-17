from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.referral.entity import ReferrerProfile
from domain.referral.port.profile_repository import ReferrerProfileRepository
from domain.user.value_object import UserId
from infra.framework.sql_alchemy.table.referral import referrer_profile_table


class ReferrerProfileRepositoryImpl(ReferrerProfileRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add(self, profile: ReferrerProfile) -> None:
        self._session.add(profile)

    async def get(self, user_id: UserId) -> ReferrerProfile | None:
        stmt = select(ReferrerProfile).where(
            referrer_profile_table.c.user_id == user_id.value,
        )
        result = await self._session.scalar(stmt)

        return result or None
