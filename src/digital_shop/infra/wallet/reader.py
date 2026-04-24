from typing import Any

from app.common.dto.money import MoneyDTO
from app.common.dto.query_params import SortingError, SortingOrder
from app.wallet.dto.sorting import WalletSortingParams
from app.wallet.dto.wallet import WalletDTO
from app.wallet.port import WalletReader
from domain.user.value_object import UserId
from infra.framework.sql_alchemy.table.wallet import wallet_table
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SortingParamsMapper:
    @classmethod
    def map(cls, src: str) -> str:
        if src == "currency":
            return "balance_currency"
        raise ValueError


class WalletReaderImpl(WalletReader):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def read_by_user_id(
        self,
        user_id: UserId,
        sorting: WalletSortingParams,
    ) -> list[WalletDTO]:
        sorting_col = wallet_table.c.get(
            SortingParamsMapper.map(sorting.field),
        )
        if sorting_col is None:
            raise SortingError(f"Invalid sorting field: '{sorting.field}'")

        order_by = (
            sorting_col.asc()
            if sorting.order == SortingOrder.ASC
            else sorting_col.desc()
        )

        stmt = (
            select(
                wallet_table.c.id,
                wallet_table.c.user_id,
                wallet_table.c.balance_currency,
                wallet_table.c.balance_amount,
            )
            .where(wallet_table.c.user_id == user_id.value)
            .order_by(order_by)
        )
        result = await self._session.execute(stmt)
        rows = result.all()

        return [self._to_dto(row) for row in rows]

    def _to_dto(self, row: Any) -> WalletDTO:
        return WalletDTO(
            id=row.id,
            user_id=row.user_id,
            currency=row.balance_currency,
            balance=MoneyDTO(
                currency=row.balance_currency,
                amount=row.balance_amount,
            ),
        )
