from decimal import Decimal
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.money import MoneyDTO
from app.common.dto.period import TimePeriod
from app.report.dto.general_report import (
    GeneralReport,
    ProductsReport,
    SalesReport,
    TopUpsReport,
)
from app.report.port import Reporter
from domain.common.money import Currency
from domain.order.enums import OrderStatus
from domain.payment.enums import PaymentPurposeType, PaymentStatus
from infra.framework.sql_alchemy.table.category import category_table
from infra.framework.sql_alchemy.table.order import order_table
from infra.framework.sql_alchemy.table.payment import payment_table
from infra.framework.sql_alchemy.table.position import (
    item_table,
    position_table,
)
from infra.framework.sql_alchemy.table.user import user_table


class ReporterImpl(Reporter):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def report_general_by_period(
        self, period: TimePeriod | None
    ) -> GeneralReport:
        new_users = await self._count_new_users(period)
        sales = await self._report_sales(period)
        top_ups = await self._report_top_ups(period)
        products = await self._report_products(period)

        return GeneralReport(
            new_users=new_users,
            sales=sales,
            top_ups=top_ups,
            products=products,
        )

    async def _count_new_users(self, period: TimePeriod | None) -> int:
        stmt = select(func.count(user_table.c.id))
        if period is not None:
            stmt = stmt.where(
                user_table.c.reg_at.between(period.from_date, period.to_date)
            )

        return (await self._session.scalar(stmt)) or 0

    async def _report_sales(self, period: TimePeriod | None) -> SalesReport:
        stmt = select(
            order_table.c.total_currency,
            func.count(order_table.c.id).label("count"),
            func.sum(order_table.c.total_amount).label("amount"),
        ).where(
            order_table.c.status == OrderStatus.CONFIRMED,
        )
        if period is not None:
            stmt = stmt.where(
                order_table.c.confirmed_at.between(
                    period.from_date, period.to_date
                ),
            )
        stmt = stmt.group_by(order_table.c.total_currency)

        rows = (await self._session.execute(stmt)).all()
        total_count, amount = self._aggregate_money(
            rows, "total_currency", "amount"
        )

        return SalesReport(count=total_count, amount=amount)

    async def _report_top_ups(self, period: TimePeriod | None) -> TopUpsReport:
        stmt = select(
            payment_table.c.original_amount_currency,
            func.count(payment_table.c.id).label("count"),
            func.sum(payment_table.c.original_amount_amount).label("amount"),
        ).where(
            payment_table.c.purpose_type == PaymentPurposeType.WALLET_TOP_UP,
            payment_table.c.status == PaymentStatus.CONFIRMED,
        )
        if period is not None:
            stmt = stmt.where(
                payment_table.c.created_at.between(
                    period.from_date, period.to_date
                ),
            )
        stmt = stmt.group_by(payment_table.c.original_amount_currency)

        rows = (await self._session.execute(stmt)).all()
        total_count, amount = self._aggregate_money(
            rows, "original_amount_currency", "amount"
        )

        return TopUpsReport(count=total_count, amount=amount)

    async def _report_products(
        self, period: TimePeriod | None
    ) -> ProductsReport:
        items_stmt = select(func.count(item_table.c.id))
        positions_stmt = select(func.count(position_table.c.id))
        categories_stmt = select(func.count(category_table.c.id))

        if period is not None:
            items_stmt = items_stmt.where(
                item_table.c.created_at.between(
                    period.from_date, period.to_date
                )
            )
            positions_stmt = positions_stmt.where(
                position_table.c.created_at.between(
                    period.from_date, period.to_date
                )
            )
            categories_stmt = categories_stmt.where(
                category_table.c.created_at.between(
                    period.from_date, period.to_date
                )
            )

        stmt = select(
            items_stmt.scalar_subquery().label("items_count"),
            positions_stmt.scalar_subquery().label("position_count"),
            categories_stmt.scalar_subquery().label("category_count"),
        )

        row = (await self._session.execute(stmt)).one()

        return ProductsReport(
            items_count=row.items_count or 0,
            position_count=row.position_count or 0,
            category_count=row.category_count or 0,
        )

    def _aggregate_money(
        self, rows: Any, currency_field: str, amount_field: str
    ) -> tuple[int, dict[Currency, MoneyDTO]]:
        total_count = sum(row.count for row in rows)

        amount: dict[Currency, MoneyDTO] = {
            getattr(row, currency_field): MoneyDTO(
                amount=getattr(row, amount_field) or Decimal("0.00"),
                currency=getattr(row, currency_field),
            )
            for row in rows
        }

        return total_count, amount
