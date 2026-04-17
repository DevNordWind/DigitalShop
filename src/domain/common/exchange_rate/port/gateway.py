from abc import ABC, abstractmethod
from collections.abc import Sequence

from domain.common.exchange_rate.value_object import CurrencyPair, ExchangeRate


class ExchangeRateGateway(ABC):
    @abstractmethod
    async def get(self, pair: CurrencyPair) -> ExchangeRate:
        raise NotImplementedError

    @abstractmethod
    async def get_many(
        self,
        pairs: Sequence[CurrencyPair],
    ) -> list[ExchangeRate]:
        raise NotImplementedError
