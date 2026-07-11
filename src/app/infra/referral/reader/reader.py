from typing import override

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.app.common.dto.query_params import (
    OffsetPaginationParams,
    SortingError,
    SortingOrder,
)
from app.app.referral.dto.award import ReferralAwardDTO
from app.app.referral.dto.paginated import ReferralAwardsPaginated
from app.app.referral.dto.sorting import ReferralAwardSortingParams
from app.app.referral.port import ReferralAwardReader
from app.domain.referral.value_object import ReferralAwardId
from app.domain.user.value_object import UserId
from app.infra.framework.sql_alchemy.table.referral import referral_award_table
from app.infra.referral.reader.mapper import ReferralAwardReaderMapper
from app.infra.referral.reader.select import REFERRAL_AWARD_SELECT


class SqlAReferralAwardReader(ReferralAwardReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def read_by_referrer_id(
        self,
        referrer_id: UserId,
        sorting: ReferralAwardSortingParams,
        pagination: OffsetPaginationParams,
    ) -> ReferralAwardsPaginated:
        sorting_col = referral_award_table.c.get(sorting.field)
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = (
            select(
                *REFERRAL_AWARD_SELECT,
                func.count().over().label("total"),
            )
            .where(referral_award_table.c.referrer_id == referrer_id)
            .order_by(order_by)
            .offset(pagination.offset)
            .limit(pagination.limit)
        )
        results = await self._session.execute(stmt)
        rows = results.all()
        if not rows:
            return ReferralAwardsPaginated(awards=[], total=0)

        total: int = rows[0].total

        return ReferralAwardsPaginated(
            awards=[ReferralAwardReaderMapper.to_dto(row=row) for row in rows],
            total=total,
        )

    @override
    async def read_by_id(
        self,
        award_id: ReferralAwardId,
    ) -> ReferralAwardDTO | None:
        stmt = select(*REFERRAL_AWARD_SELECT).where(
            referral_award_table.c.id == award_id,
        )
        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None

        return ReferralAwardReaderMapper.to_dto(row=row)
