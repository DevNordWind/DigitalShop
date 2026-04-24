from domain.payment.entity import Payment
from domain.payment.port import PaymentRepository
from domain.payment.value_object import PaymentId
from infra.framework.sql_alchemy.table.payment import payment_table
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class PaymentRepositoryImpl(PaymentRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add(self, payment: Payment) -> None:
        self._session.add(payment)

    async def get(self, payment_id: PaymentId) -> Payment | None:
        stmt = (
            select(Payment)
            .where(payment_table.c.id == payment_id.value)
            .with_for_update()
        )

        result = await self._session.scalar(stmt)

        return result or None
