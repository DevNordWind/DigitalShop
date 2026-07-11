from dataclasses import dataclass

from app.domain.common.money import Currency, Money


@dataclass(slots=True, frozen=True)
class SalesReport:
    count: int
    amount: dict[Currency, Money]


@dataclass(slots=True, frozen=True)
class TopUpsReport:
    count: int
    amount: dict[Currency, Money]


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
