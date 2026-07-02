from collections.abc import Sequence
from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.common.money import Currency
from app.domain.user.value_object import UserId
from app.domain.wallet.entity import Wallet
from app.domain.wallet.port import WalletRepository
from app.domain.wallet.value_object import WalletId
from app.infra.framework.sql_alchemy.table.wallet import wallet_table


class SqlAWalletRepository(WalletRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    @override
    async def add_many(self, wallets: Sequence[Wallet]) -> None:
        self._session.add_all(wallets)

    @override
    async def get_by_user_id_currency(
        self,
        user_id: UserId,
        currency: Currency,
    ) -> Wallet | None:
        stmt = select(Wallet).where(
            wallet_table.c.user_id == user_id,
            wallet_table.c.balance_currency == currency,
        )
        return await self._session.scalar(stmt)

    @override
    async def acquire(self, wallet_id: WalletId) -> Wallet | None:
        stmt = (
            select(Wallet)
            .where(
                wallet_table.c.id == wallet_id,
            )
            .with_for_update()
        )
        return await self._session.scalar(stmt)

    @override
    async def acquire_user_id_by_currency(
        self,
        user_id: UserId,
        currency: Currency,
    ) -> Wallet | None:
        stmt = (
            select(Wallet)
            .where(
                wallet_table.c.user_id == user_id,
                wallet_table.c.balance_currency == currency,
            )
            .with_for_update()
        )
        return await self._session.scalar(stmt)
