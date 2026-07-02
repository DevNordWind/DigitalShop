from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.referral.entity import ReferrerProfile
from app.domain.referral.port import ReferrerProfileRepository
from app.domain.user.value_object import UserId
from app.infra.framework.sql_alchemy.table.referral import referrer_profile_table


class SqlAReferrerProfileRepository(ReferrerProfileRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def add(self, profile: ReferrerProfile) -> None:
        self._session.add(profile)

    @override
    async def get(self, user_id: UserId) -> ReferrerProfile | None:
        stmt = select(ReferrerProfile).where(
            referrer_profile_table.c.user_id == user_id,
        )
        return await self._session.scalar(stmt)
