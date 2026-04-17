from app.common.dto.exchange_rate.pair import CurrencyPairDTO
from app.common.dto.exchange_rate.rate import ExchangeRateDTO
from domain.common.exchange_rate import CurrencyPair, ExchangeRate


class CurrencyPairMapper:
    @classmethod
    def to_dto(cls, src: CurrencyPair) -> CurrencyPairDTO:
        return CurrencyPairDTO(source=src.source, target=src.target)

    @classmethod
    def to_value_object(cls, src: CurrencyPairDTO) -> CurrencyPair:
        return CurrencyPair(source=src.source, target=src.target)


class ExchangeRateMapper:
    @classmethod
    def to_dto(cls, src: ExchangeRate) -> ExchangeRateDTO:
        return ExchangeRateDTO(
            pair=CurrencyPairMapper.to_dto(src=src.pair),
            rate=src.rate,
            timestamp=src.timestamp,
        )

    @classmethod
    def to_value_object(cls, src: ExchangeRateDTO) -> ExchangeRate:
        return ExchangeRate(
            pair=CurrencyPairMapper.to_value_object(src=src.pair),
            rate=src.rate,
            timestamp=src.timestamp,
        )
