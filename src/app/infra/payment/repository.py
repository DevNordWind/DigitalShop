from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.payment.entity import Payment
from app.domain.payment.port import PaymentRepository
from app.domain.payment.value_object import PaymentId
from app.infra.framework.sql_alchemy.table.payment import payment_table


class SqlAPaymentRepository(PaymentRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def add(self, payment: Payment) -> None:
        self._session.add(payment)

    @override
    async def acquire(self, payment_id: PaymentId) -> Payment | None:
        stmt = select(Payment).where(payment_table.c.id == payment_id).with_for_update()

        return await self._session.scalar(stmt)
