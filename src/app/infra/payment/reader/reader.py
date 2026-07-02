from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.app.payment.dto.payment import PaymentDTO
from app.app.payment.port import PaymentReader
from app.domain.payment.value_object import PaymentId
from app.infra.framework.sql_alchemy.table.payment import payment_table
from app.infra.payment.reader.mapper import PaymentReaderMapper
from app.infra.payment.reader.select import PAYMENT_SELECT


class SqlAPaymentReader(PaymentReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def read(self, payment_id: PaymentId) -> PaymentDTO | None:
        stmt = select(*PAYMENT_SELECT).where(
            payment_table.c.id == payment_id,
        )

        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None

        return PaymentReaderMapper.to_dto(row=row)
