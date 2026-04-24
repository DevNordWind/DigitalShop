from app.common.dto.query_params import (
    OffsetPaginationParams,
    SortingError,
    SortingOrder,
)
from app.referral.dto.award import ReferralAwardDTO
from app.referral.dto.paginated import ReferralAwardsPaginated
from app.referral.dto.sorting import ReferralAwardSortingParams
from app.referral.port import ReferralAwardReader
from domain.referral.value_object import ReferralAwardId
from domain.user.value_object import UserId
from infra.framework.sql_alchemy.table.referral import referral_award_table
from infra.referral.reader.mapper import ReferralAwardReaderMapper
from infra.referral.reader.select import REFERRAL_AWARD_SELECT
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class ReferralAwardReaderImpl(ReferralAwardReader):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

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
            .where(referral_award_table.c.referrer_id == referrer_id.value)
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

    async def read_by_id(
        self,
        award_id: ReferralAwardId,
    ) -> ReferralAwardDTO | None:
        stmt = select(*REFERRAL_AWARD_SELECT).where(
            referral_award_table.c.id == award_id.value,
        )
        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None

        return ReferralAwardReaderMapper.to_dto(row=row)
