from typing import override
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.referral.entity import ReferralAward
from app.domain.referral.port import ReferralAwardRepository
from app.domain.referral.value_object import ReferralAwardId
from app.infra.framework.sql_alchemy.table.referral import referral_award_table


class SqlAReferralAwardRepository(ReferralAwardRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def add(self, award: ReferralAward) -> None:
        self._session.add(award)

    @override
    async def get(self, award_id: ReferralAwardId) -> ReferralAward | None:
        stmt = select(ReferralAward).where(
            referral_award_table.c.id == award_id,
        )
        return await self._session.scalar(stmt)

    @override
    async def get_by_reference_id(self, reference_id: UUID) -> ReferralAward | None:
        stmt = select(ReferralAward).where(
            referral_award_table.c.source_reference_id == reference_id,
        )
        return await self._session.scalar(stmt)
