from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.common.money import Currency
from domain.user.value_object import UserId
from domain.wallet.entity import Wallet
from domain.wallet.port import WalletRepository
from domain.wallet.value_object import WalletId
from infra.framework.sql_alchemy.table.wallet import wallet_table


class WalletRepositoryImpl(WalletRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add_many(self, wallets: Sequence[Wallet]) -> None:
        self._session.add_all(wallets)

    async def get(self, wallet_id: WalletId) -> Wallet | None:
        stmt = select(Wallet).where(wallet_table.c.id == wallet_id.value)
        result = await self._session.scalar(stmt)

        return result or None

    async def get_by_currency_for_update(
        self,
        user_id: UserId,
        currency: Currency,
    ) -> Wallet | None:
        stmt = (
            select(Wallet)
            .where(
                wallet_table.c.user_id == user_id.value,
                wallet_table.c.balance_currency == currency,
            )
            .with_for_update()
        )
        result = await self._session.scalar(stmt)

        return result or None
