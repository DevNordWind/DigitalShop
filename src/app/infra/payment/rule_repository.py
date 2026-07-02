from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.app.payment.exception import PaymentCommissionRuleNotCreatedError
from app.domain.payment.enums import PaymentMethod
from app.domain.payment.port import PaymentCommissionRuleRepository
from app.domain.payment.rule import PaymentCommissionRule
from app.infra.framework.sql_alchemy.table.payment import payment_commission_rule_table


class SqlAPaymentCommissionRuleRepository(PaymentCommissionRuleRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def add(self, rule: PaymentCommissionRule) -> None:
        self._session.add(rule)

    @override
    async def merge(
        self,
        old_rule: PaymentCommissionRule,
        new_rule: PaymentCommissionRule,
    ) -> None:
        await self._session.delete(old_rule)
        self._session.add(new_rule)

    @override
    async def get(self, method: PaymentMethod) -> PaymentCommissionRule:
        stmt = select(PaymentCommissionRule).where(
            payment_commission_rule_table.c.payment_method == method,
        )
        result = await self._session.scalar(stmt)
        if not result:
            raise PaymentCommissionRuleNotCreatedError

        return result
