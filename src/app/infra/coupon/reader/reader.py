from datetime import datetime
from typing import Any, override

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.app.common.dto.query_params import (
    OffsetPaginationParams,
    SortingError,
    SortingOrder,
)
from app.app.coupon.dto.coupon import CouponDTO
from app.app.coupon.dto.paginated import CouponsPaginated
from app.app.coupon.dto.sorting import CouponSortingParams
from app.app.coupon.port import CouponReader
from app.domain.coupon.enums import CouponStatus
from app.domain.coupon.value_object import CouponId
from app.infra.coupon.reader.mapper import CouponReaderMapper
from app.infra.coupon.reader.select import COUPON_SELECT
from app.infra.framework.sql_alchemy.table.coupon import coupon_table


class SqlACouponReader(CouponReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def read(self, coupon_id: CouponId) -> CouponDTO | None:
        stmt = select(*COUPON_SELECT).where(
            coupon_table.c.id == coupon_id,
        )
        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None

        return CouponReaderMapper.to_dto(row=row)

    @override
    async def read_paginated(
        self,
        sorting: CouponSortingParams,
        pagination: OffsetPaginationParams,
        status: CouponStatus | None,
        now: datetime,
    ) -> CouponsPaginated:
        sorting_col = coupon_table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = select(
            *COUPON_SELECT,
            func.count().over().label("total"),
        )
        if status is not None:
            stmt = stmt.where(*self._build_status_filters(status, now))

        stmt = stmt.order_by(order_by).limit(pagination.limit).offset(pagination.offset)
        result = await self._session.execute(stmt)
        rows = result.all()
        if not rows:
            return CouponsPaginated(coupons=[], total=0)

        total: int = rows[0].total

        return CouponsPaginated(
            coupons=[CouponReaderMapper.to_dto(row=row) for row in rows],
            total=total,
        )

    def _build_status_filters(
        self,
        status: CouponStatus,
        now: datetime,
    ) -> tuple[Any, ...]:
        c = coupon_table.c
        match status:
            case CouponStatus.ACTIVE:
                return (
                    c.is_revoked.is_(False),
                    c.valid_from <= now,
                    (c.valid_until.is_(None)) | (c.valid_until > now),
                )
            case CouponStatus.REVOKED:
                return (c.is_revoked.is_(True),)
            case CouponStatus.EXPIRED:
                return (
                    c.is_revoked.is_(False),
                    c.valid_until.is_not(None),
                    c.valid_until <= now,
                )
            case CouponStatus.NOT_STARTED:
                return (
                    c.is_revoked.is_(False),
                    c.valid_from > now,
                )
