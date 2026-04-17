from frozendict import frozendict

from app.common.dto.coefficient import CoefficientMapper
from app.common.dto.money import MoneyMapper
from app.coupon.dto.discount import (
    CoefficientDiscountDTO,
    DiscountDTO,
    FixedAmountDiscountDTO,
)
from domain.common.money import Currency, Money
from domain.coupon.enums import CouponType
from domain.coupon.strategy import (
    CoefficientDiscount,
    DiscountStrategy,
    FixedAmountDiscount,
)


class DiscountMapper:
    @classmethod
    def to_strategy(cls, src: DiscountDTO) -> DiscountStrategy:
        match src:
            case FixedAmountDiscountDTO():
                return cls._to_fixed(src)
            case CoefficientDiscountDTO():
                return cls._to_coefficient(src)

    @classmethod
    def to_dto(cls, src: DiscountStrategy) -> DiscountDTO:
        match src:
            case FixedAmountDiscount():
                return cls._to_fixed_dto(src)
            case CoefficientDiscount():
                return cls._to_coefficient_dto(src)

        raise ValueError

    @staticmethod
    def _to_fixed(src: FixedAmountDiscountDTO) -> FixedAmountDiscount:
        discounts: dict[Currency, Money] = {}
        for currency, money_dto in src.discounts.items():
            discounts[currency] = MoneyMapper.to_value_object(src=money_dto)

        return FixedAmountDiscount(discounts=frozendict(discounts))

    @staticmethod
    def _to_coefficient(src: CoefficientDiscountDTO) -> CoefficientDiscount:
        return CoefficientDiscount(
            coefficient=CoefficientMapper.to_value_object(src.coefficient),
        )

    @staticmethod
    def _to_fixed_dto(src: FixedAmountDiscount) -> FixedAmountDiscountDTO:
        return FixedAmountDiscountDTO(
            discounts={
                currency: MoneyMapper.to_dto(src=money)
                for currency, money in src.discounts.items()
            },
            type=CouponType.FIXED,
        )

    @staticmethod
    def _to_coefficient_dto(
        src: CoefficientDiscount,
    ) -> CoefficientDiscountDTO:
        return CoefficientDiscountDTO(
            coefficient=CoefficientMapper.to_dto(src.coefficient),
            type=CouponType.COEFFICIENT,
        )
