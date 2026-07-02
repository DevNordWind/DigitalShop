from dataclasses import dataclass

from app.app.common.dto.money import MoneyMapper
from app.app.common.dto.period import TimePeriodDTO, TimePeriodMapper
from app.app.common.port.actor_provider import ActorProvider
from app.app.report.dto.general import (
    ConvertedGeneralReportDTO,
    ConvertedSalesReportDTO,
    ConvertedTopUpsReportDTO,
    ProductsReportMapper,
)
from app.domain.common.exchange_rate import (
    CurrencyPair,
    ExchangeRate,
    ExchangeRateGateway,
)
from app.domain.common.exchange_rate.service import MoneyConverter
from app.domain.common.money import Currency
from app.domain.report.port import Reporter
from app.domain.report.report import GeneralReport
from app.domain.report.service.access import ReportAccessService


@dataclass(slots=True, frozen=True)
class GetConvertedGeneralReportQuery:
    period: TimePeriodDTO | None
    convert_to: Currency


class GetConvertedGeneralReport:
    def __init__(
        self,
        reporter: Reporter,
        actor_provider: ActorProvider,
        rate_gw: ExchangeRateGateway,
    ) -> None:
        self._reporter = reporter
        self._actor_provider = actor_provider
        self._rate_gw = rate_gw

    async def __call__(
        self, query: GetConvertedGeneralReportQuery
    ) -> ConvertedGeneralReportDTO:
        ReportAccessService.ensure_can_get_general(
            actor=await self._actor_provider.get()
        )

        report: GeneralReport = await self._reporter.report_general_by_period(
            period=TimePeriodMapper.to_value_object(src=query.period)
            if query.period
            else None
        )
        rates: tuple[ExchangeRate, ...] = await self._rate_gw.get_many(
            pairs=[
                CurrencyPair(source=currency, target=query.convert_to)
                for currency in report.sales.amount.keys()
                | report.top_ups.amount.keys()
                if currency != query.convert_to
            ]
        )

        return ConvertedGeneralReportDTO(
            new_users=report.new_users,
            products=ProductsReportMapper.to_dto(src=report.products),
            sales=ConvertedSalesReportDTO(
                count=report.sales.count,
                amount=MoneyMapper.to_dto(
                    src=MoneyConverter.convert_many(
                        amounts=report.sales.amount,
                        rates=rates,
                        target=query.convert_to,
                    )
                ),
            ),
            top_ups=ConvertedTopUpsReportDTO(
                count=report.top_ups.count,
                amount=MoneyMapper.to_dto(
                    src=MoneyConverter.convert_many(
                        amounts=report.top_ups.amount,
                        rates=rates,
                        target=query.convert_to,
                    )
                ),
            ),
        )
