from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.payment.enums import PaymentMethod
from domain.payment.exception import PaymentCommissionRuleNotCreated
from domain.payment.port import PaymentCommissionRuleRepository
from domain.payment.rule import PaymentCommissionRule
from infra.framework.sql_alchemy.table.payment import (
    payment_commission_rule_table,
)


class PaymentCommissionRuleRepositoryImpl(PaymentCommissionRuleRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add(self, rule: PaymentCommissionRule) -> None:
        self._session.add(rule)

    async def merge(
        self,
        old_rule: PaymentCommissionRule,
        new_rule: PaymentCommissionRule,
    ) -> None:
        await self._session.delete(old_rule)
        self._session.add(new_rule)

    async def get(self, method: PaymentMethod) -> PaymentCommissionRule:
        stmt = select(PaymentCommissionRule).where(
            payment_commission_rule_table.c.payment_method == method,
        )
        result = await self._session.scalar(stmt)
        if not result:
            raise PaymentCommissionRuleNotCreated

        return result
