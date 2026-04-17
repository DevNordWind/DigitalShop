from dataclasses import dataclass
from decimal import Decimal

from app.common.dto.money import MoneyDTO, MoneyMapper
from app.common.exception import DataCorruptionError
from app.user.port import UserIdentifyProvider
from app.wallet.dto.sorting import WalletSortingParams
from app.wallet.dto.wallet import WalletDTO
from app.wallet.port import WalletReader
from domain.common.exchange_rate import (
    CurrencyPair,
    ExchangeRateGateway,
    ExchangeRateNotFound,
)
from domain.common.money import Currency, Money


@dataclass(slots=True, frozen=True)
class GetMyWalletsWithTotalQuery:
    sorting: WalletSortingParams
    target_total: Currency


@dataclass(slots=True, frozen=True)
class WalletsWithTotal:
    wallets: list[WalletDTO]
    total: MoneyDTO


class GetMyWalletsWithTotal:
    def __init__(
        self,
        idp: UserIdentifyProvider,
        reader: WalletReader,
        rate_gateway: ExchangeRateGateway,
    ):
        self._idp: UserIdentifyProvider = idp
        self._rate_gateway: ExchangeRateGateway = rate_gateway
        self._reader: WalletReader = reader

    async def __call__(
        self,
        query: GetMyWalletsWithTotalQuery,
    ) -> WalletsWithTotal:
        wallets: list[WalletDTO] = await self._reader.read_by_user_id(
            user_id=await self._idp.get_user_id(),
            sorting=query.sorting,
        )
        if not wallets:
            raise DataCorruptionError

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
                raise ExchangeRateNotFound
            total = total + rate.convert(balance)

        return WalletsWithTotal(
            wallets=wallets,
            total=MoneyMapper.to_dto(total),
        )
