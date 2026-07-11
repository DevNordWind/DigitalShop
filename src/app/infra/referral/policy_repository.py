from typing import override

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.app.referral.exception import ReferralPolicyNotCreatedError
from app.domain.referral.policy import ReferralPolicy
from app.domain.referral.port import ReferralPolicyRepository
from app.infra.framework.sql_alchemy.table.referral import referral_policy_table


class SqlAReferralPolicyRepository(ReferralPolicyRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def add(self, policy: ReferralPolicy) -> None:
        self._session.add(policy)

    @override
    async def get(self) -> ReferralPolicy:
        stmt = (
            select(ReferralPolicy)
            .limit(1)
            .order_by(desc(referral_policy_table.c.current_version))
        )

        result = await self._session.scalar(stmt)
        if not result:
            raise ReferralPolicyNotCreatedError

        return result

    @override
    async def acquire(self) -> ReferralPolicy:
        stmt = (
            select(ReferralPolicy)
            .limit(1)
            .order_by(desc(referral_policy_table.c.current_version))
        ).with_for_update()

        result = await self._session.scalar(stmt)
        if result is None:
            raise ReferralPolicyNotCreatedError

        return result
