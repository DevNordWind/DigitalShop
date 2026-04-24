from dataclasses import dataclass

from app.common.dto.money import MoneyDTO
from domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class SalesReport:
    count: int
    amount: dict[Currency, MoneyDTO]


@dataclass(slots=True, frozen=True)
class TopUpsReport:
    count: int
    amount: dict[Currency, MoneyDTO]


@dataclass(slots=True, frozen=True)
class ConvertedSalesReport:
    count: int
    amount: MoneyDTO


@dataclass(slots=True, frozen=True)
class ConvertedTopUpsReport:
    count: int
    amount: MoneyDTO


@dataclass(slots=True, frozen=True)
class ProductsReport:
    items_count: int
    position_count: int
    category_count: int


@dataclass(slots=True, frozen=True)
class GeneralReport:
    new_users: int

    sales: SalesReport
    top_ups: TopUpsReport
    products: ProductsReport


@dataclass(slots=True, frozen=True)
class ConvertedGeneralReport:
    new_users: int

    sales: ConvertedSalesReport
    top_ups: ConvertedTopUpsReport
    products: ProductsReport
