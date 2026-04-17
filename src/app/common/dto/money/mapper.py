from app.common.dto.money.dto import MoneyDTO
from domain.common.money import Money


class MoneyMapper:
    @classmethod
    def to_value_object(cls, src: MoneyDTO) -> Money:
        return Money(amount=src.amount, currency=src.currency)

    @classmethod
    def to_dto(cls, src: Money) -> MoneyDTO:
        return MoneyDTO(amount=src.amount, currency=src.currency)
