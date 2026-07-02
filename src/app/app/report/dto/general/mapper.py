from app.app.common.dto.money import MoneyMapper
from app.app.report.dto.general.general_report import (
    GeneralReportDTO,
    ProductsReportDTO,
    SalesReportDTO,
    TopUpsReportDTO,
)
from app.domain.report.report import (
    GeneralReport,
    ProductsReport,
    SalesReport,
    TopUpsReport,
)


class SalesReportMapper:
    @classmethod
    def to_dto(cls, src: SalesReport) -> SalesReportDTO:
        return SalesReportDTO(
            count=src.count,
            amount={
                currency: MoneyMapper.to_dto(src=money)
                for currency, money in src.amount.items()
            },
        )


class TopUpsReportMapper:
    @classmethod
    def to_dto(cls, src: TopUpsReport) -> TopUpsReportDTO:
        return TopUpsReportDTO(
            count=src.count,
            amount={
                currency: MoneyMapper.to_dto(src=money)
                for currency, money in src.amount.items()
            },
        )


class ProductsReportMapper:
    @classmethod
    def to_dto(cls, src: ProductsReport) -> ProductsReportDTO:
        return ProductsReportDTO(
            items_count=src.items_count,
            position_count=src.position_count,
            category_count=src.category_count,
        )


class GeneralReportMapper:
    @classmethod
    def to_dto(cls, src: GeneralReport) -> GeneralReportDTO:
        return GeneralReportDTO(
            new_users=src.new_users,
            sales=SalesReportMapper.to_dto(src=src.sales),
            top_ups=TopUpsReportMapper.to_dto(src=src.top_ups),
            products=ProductsReportMapper.to_dto(src=src.products),
        )
