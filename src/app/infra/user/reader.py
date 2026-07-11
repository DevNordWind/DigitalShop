from typing import override

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.app.user.dto import UserProfileDTO
from app.app.user.port import UserReader
from app.domain.order.enums import OrderStatus
from app.domain.payment.enums import PaymentPurposeType, PaymentStatus
from app.domain.user.value_object import UserId
from app.infra.framework.sql_alchemy.table.order import order_table
from app.infra.framework.sql_alchemy.table.payment import payment_table
from app.infra.framework.sql_alchemy.table.user import user_table


class SqlAUserReader(UserReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def read_profile(self, user_id: UserId) -> UserProfileDTO | None:
        orders_count_stmt = (
            select(func.count(order_table.c.id))
            .where(
                order_table.c.customer_id == user_id,
                order_table.c.status == OrderStatus.CONFIRMED,
            )
            .scalar_subquery()
        )

        top_ups_count_stmt = (
            select(func.count(payment_table.c.id))
            .where(
                payment_table.c.creator_id == user_id,
                payment_table.c.purpose_type == PaymentPurposeType.WALLET_TOP_UP,
                payment_table.c.status == PaymentStatus.CONFIRMED,
            )
            .scalar_subquery()
        )

        stmt = select(
            user_table.c.id,
            user_table.c.role,
            user_table.c.reg_at,
            orders_count_stmt.label("orders_count"),
            top_ups_count_stmt.label("top_ups_count"),
        ).where(user_table.c.id == user_id)

        result = await self._session.execute(stmt)
        row = result.one_or_none()

        if not row:
            return None

        return UserProfileDTO(
            id=row.id.value,
            role=row.role,
            reg_at=row.reg_at,
            orders_count=row.orders_count or 0,
            top_ups_count=row.top_ups_count or 0,
        )
