from dataclasses import dataclass

from app.app.common.dto.money import MoneyDTO
from app.domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class SalesReportDTO:
    count: int
    amount: dict[Currency, MoneyDTO]


@dataclass(slots=True, frozen=True)
class TopUpsReportDTO:
    count: int
    amount: dict[Currency, MoneyDTO]


@dataclass(slots=True, frozen=True)
class ConvertedSalesReportDTO:
    count: int
    amount: MoneyDTO


@dataclass(slots=True, frozen=True)
class ConvertedTopUpsReportDTO:
    count: int
    amount: MoneyDTO


@dataclass(slots=True, frozen=True)
class ProductsReportDTO:
    items_count: int
    position_count: int
    category_count: int


@dataclass(slots=True, frozen=True)
class GeneralReportDTO:
    new_users: int

    sales: SalesReportDTO
    top_ups: TopUpsReportDTO
    products: ProductsReportDTO


@dataclass(slots=True, frozen=True)
class ConvertedGeneralReportDTO:
    new_users: int

    sales: ConvertedSalesReportDTO
    top_ups: ConvertedTopUpsReportDTO
    products: ProductsReportDTO
