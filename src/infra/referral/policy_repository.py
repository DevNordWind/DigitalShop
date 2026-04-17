from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.referral.exception import ReferralPolicyNotCreated
from domain.referral.policy import ReferralPolicy
from domain.referral.port import (
    ReferralPolicyRepository,
)
from infra.framework.sql_alchemy.table.referral import (
    referral_policy_table,
)


class ReferralPolicyRepositoryImpl(ReferralPolicyRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add(self, policy: ReferralPolicy) -> None:
        self._session.add(policy)

    async def get(self) -> ReferralPolicy:
        stmt = (
            select(ReferralPolicy)
            .limit(1)
            .order_by(desc(referral_policy_table.c.current_version))
        )

        result = await self._session.scalar(stmt)
        if not result:
            raise ReferralPolicyNotCreated

        return result

    async def get_for_update(self) -> ReferralPolicy:
        stmt = (
            select(ReferralPolicy)
            .limit(1)
            .order_by(desc(referral_policy_table.c.current_version))
        ).with_for_update()

        result = await self._session.scalar(stmt)
        if result is None:
            raise ReferralPolicyNotCreated

        return result
