from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from app.app.common.dto.money import MoneyDTO, MoneyMapper
from app.app.common.port.actor_provider import ActorProvider
from app.app.wallet.dto import WalletDTO, WalletSortingParams
from app.app.wallet.port import WalletReader
from app.domain.common.exchange_rate import (
    CurrencyPair,
    ExchangeRateGateway,
    ExchangeRateNotFoundError,
)
from app.domain.common.money import Currency, Money
from app.domain.user.exception import UserNotFoundError
from app.domain.user.value_object import UserId
from app.domain.wallet.service import WalletAccessService


@dataclass(slots=True, frozen=True)
class GetWalletsByUserIdWithTotalQuery:
    target_user_id: UUID

    sorting: WalletSortingParams
    target_total: Currency


@dataclass(slots=True, frozen=True)
class WalletsWithTotal:
    wallets: list[WalletDTO]
    total: MoneyDTO


class GetWalletsByUserIdWithTotal:
    def __init__(
        self,
        actor_provider: ActorProvider,
        reader: WalletReader,
        rate_gateway: ExchangeRateGateway,
    ):
        self._actor_provider = actor_provider
        self._rate_gateway = rate_gateway
        self._reader = reader

    async def __call__(
        self,
        query: GetWalletsByUserIdWithTotalQuery,
    ) -> WalletsWithTotal:
        target_user_id = UserId(query.target_user_id)

        WalletAccessService.ensure_can_view(
            actor=await self._actor_provider.get(), target_user_id=target_user_id
        )
        wallets: list[WalletDTO] = await self._reader.read_by_user_id(
            user_id=target_user_id,
            sorting=query.sorting,
        )
        if not wallets:
            raise UserNotFoundError

        pairs: list[CurrencyPair] = [
            CurrencyPair(
                source=wallet.balance.currency,
                target=query.target_total,
            )
            for wallet in wallets
            if wallet.balance.currency != query.target_total
        ]
        fetched = await self._rate_gateway.get_many(pairs=pairs)
        rates = {rate.pair: rate for rate in fetched}

        total = Money(amount=Decimal(0), currency=query.target_total)

        for wallet in wallets:
            balance = MoneyMapper.to_value_object(src=wallet.balance)
            if balance.currency == query.target_total:
                total = total + balance
                continue
            pair = CurrencyPair(
                source=balance.currency,
                target=query.target_total,
            )
            rate = rates.get(pair)
            if rate is None:
                raise ExchangeRateNotFoundError

            total = total + rate.convert(balance)

        return WalletsWithTotal(
            wallets=wallets,
            total=MoneyMapper.to_dto(total),
        )
