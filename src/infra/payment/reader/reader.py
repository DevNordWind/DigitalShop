from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.payment.dto.payment import PaymentDTO
from app.payment.port import PaymentReader
from domain.payment.value_object import PaymentId
from infra.framework.sql_alchemy.table.payment import payment_table
from infra.payment.reader.mapper import PaymentReaderMapper
from infra.payment.reader.select import PAYMENT_SELECT


class PaymentReaderImpl(PaymentReader):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def read(self, payment_id: PaymentId) -> PaymentDTO | None:
        stmt = select(*PAYMENT_SELECT).where(
            payment_table.c.id == payment_id.value,
        )

        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None

        return PaymentReaderMapper.to_dto(row=row)
