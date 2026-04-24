from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal

from app.common.dto.money import MoneyDTO, MoneyMapper
from app.common.dto.period import TimePeriod
from app.report.dto.general_report import (
    ConvertedGeneralReport,
    ConvertedSalesReport,
    ConvertedTopUpsReport,
    GeneralReport,
)
from app.report.exception import ReporterPermissionDenied
from app.report.port import Reporter
from app.report.service.access import ReporterAccessService
from app.user.port import UserIdentifyProvider
from domain.common.exchange_rate import (
    CurrencyPair,
    ExchangeRate,
    ExchangeRateGateway,
)
from domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class GetConvertedGeneralReportQuery:
    period: TimePeriod | None
    convert_to: Currency


class GetConvertedGeneralReport:
    def __init__(
        self,
        reporter: Reporter,
        idp: UserIdentifyProvider,
        rate_gw: ExchangeRateGateway,
    ) -> None:
        self._reporter = reporter
        self._idp = idp
        self._rate_gw = rate_gw

    async def __call__(
        self, query: GetConvertedGeneralReportQuery
    ) -> ConvertedGeneralReport:
        if not ReporterAccessService.can_get_general(
            role=await self._idp.get_role()
        ):
            raise ReporterPermissionDenied

        report: GeneralReport = await self._reporter.report_general_by_period(
            period=query.period
        )
        rate_map = await self._build_rate_map(
            currencies=report.sales.amount.keys()
            | report.top_ups.amount.keys(),
            target=query.convert_to,
        )

        return ConvertedGeneralReport(
            new_users=report.new_users,
            products=report.products,
            sales=ConvertedSalesReport(
                count=report.sales.count,
                amount=self._convert_amount(
                    report.sales.amount, rate_map, query.convert_to
                ),
            ),
            top_ups=ConvertedTopUpsReport(
                count=report.top_ups.count,
                amount=self._convert_amount(
                    report.top_ups.amount, rate_map, query.convert_to
                ),
            ),
        )

    async def _build_rate_map(
        self,
        currencies: Iterable[Currency],
        target: Currency,
    ) -> dict[Currency, ExchangeRate]:
        pairs = [
            CurrencyPair(source=currency, target=target)
            for currency in currencies
            if currency != target
        ]
        if not pairs:
            return {}
        rates = await self._rate_gw.get_many(pairs)
        return {rate.pair.source: rate for rate in rates}

    def _convert_amount(
        self,
        amounts: dict[Currency, MoneyDTO],
        rate_map: dict[Currency, ExchangeRate],
        target: Currency,
    ) -> MoneyDTO:
        if not amounts:
            return MoneyDTO(currency=target, amount=Decimal("0.00"))

        total = Decimal("0.00")
        for currency, money_dto in amounts.items():
            money_vo = MoneyMapper.to_value_object(src=money_dto)
            if currency == target:
                total += money_vo.amount
                continue
            total += rate_map[currency].convert(money_vo).amount

        return MoneyDTO(currency=target, amount=total)
