from app.user.dto.report import UserProfileReport
from app.user.port.reporter import UserReporter
from domain.order.enums import OrderStatus
from domain.payment.enums import PaymentPurposeType, PaymentStatus
from domain.user.value_object import UserId
from infra.framework.sql_alchemy.table.order import order_table
from infra.framework.sql_alchemy.table.payment import payment_table
from infra.framework.sql_alchemy.table.user import user_table
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class UserReporterImpl(UserReporter):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def report_profile(
        self, target_user_id: UserId
    ) -> UserProfileReport | None:
        orders_count_stmt = (
            select(func.count(order_table.c.id))
            .where(
                order_table.c.customer_id == target_user_id.value,
                order_table.c.status == OrderStatus.CONFIRMED,
            )
            .scalar_subquery()
        )

        top_ups_count_stmt = (
            select(func.count(payment_table.c.id))
            .where(
                payment_table.c.creator_id == target_user_id.value,
                payment_table.c.purpose_type
                == PaymentPurposeType.WALLET_TOP_UP,
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
        ).where(user_table.c.id == target_user_id.value)

        result = await self._session.execute(stmt)
        row = result.one_or_none()

        if not row:
            return None

        return UserProfileReport(
            id=row.id,
            role=row.role,
            reg_at=row.reg_at,
            orders_count=row.orders_count or 0,
            top_ups_count=row.top_ups_count or 0,
        )
