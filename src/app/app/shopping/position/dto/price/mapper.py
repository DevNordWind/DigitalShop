from frozendict import frozendict

from app.app.common.dto.money import MoneyMapper
from app.app.shopping.position.dto.price.dto import PositionPriceDTO
from app.domain.shopping.position.value_object import PositionPrice


class PositionPriceMapper:
    @classmethod
    def to_value_object(cls, src: PositionPriceDTO) -> PositionPrice:
        return PositionPrice(
            base_currency=src.base_currency,
            prices=frozendict(
                (currency, MoneyMapper.to_value_object(src=money))
                for currency, money in src.prices.items()
            ),
        )

    @classmethod
    def to_dto(cls, src: PositionPrice) -> PositionPriceDTO:
        return PositionPriceDTO(
            base_currency=src.base_currency,
            prices={
                currency: MoneyMapper.to_dto(money)
                for currency, money in src.prices.items()
            },
        )
