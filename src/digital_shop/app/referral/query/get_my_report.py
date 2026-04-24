from dataclasses import dataclass
from decimal import Decimal

from app.common.dto.money import MoneyDTO, MoneyMapper
from app.common.dto.period import TimePeriod
from app.referral.dto.report import ConvertedReferrerReport, ReferrerReport
from app.referral.port import ReferralSystemReporter
from app.user.port import UserIdentifyProvider
from domain.common.exchange_rate import (
    CurrencyPair,
    ExchangeRate,
    ExchangeRateGateway,
    ExchangeRateNotFound,
)
from domain.common.money import Currency


@dataclass(slots=True, frozen=True)
class GetMyReferrerReportQuery:
    convert_to: Currency
    period: TimePeriod | None


class GetMyReferrerReport:
    def __init__(
        self,
        reporter: ReferralSystemReporter,
        rate_gw: ExchangeRateGateway,
        idp: UserIdentifyProvider,
    ):
        self._reporter: ReferralSystemReporter = reporter
        self._rate_gw: ExchangeRateGateway = rate_gw
        self._idp: UserIdentifyProvider = idp

    async def __call__(
        self,
        query: GetMyReferrerReportQuery,
    ) -> ConvertedReferrerReport:
        report: ReferrerReport = await self._reporter.get_referrer_report(
            referrer_id=await self._idp.get_user_id(),
            period=query.period,
        )
        if not report.awards_sum:
            return ConvertedReferrerReport(
                report=report,
                total=MoneyDTO(
                    amount=Decimal("0.00"),
                    currency=query.convert_to,
                ),
            )

        pairs: list[CurrencyPair] = [
            CurrencyPair(source=currency, target=query.convert_to)
            for currency in report.awards_sum
            if currency != query.convert_to
        ]
        rates: dict[CurrencyPair, ExchangeRate] = {
            rate.pair: rate
            for rate in await self._rate_gw.get_many(pairs=pairs)
        }

        total_amount = Decimal("0.00")

        for currency, award in report.awards_sum.items():
            if currency == query.convert_to:
                total_amount += award.amount
                continue

            pair = CurrencyPair(source=currency, target=query.convert_to)
            rate = rates.get(pair)
            if rate is None:
                raise ExchangeRateNotFound

            converted = rate.convert(
                amount=MoneyMapper.to_value_object(src=award),
            )
            total_amount += converted.amount

        return ConvertedReferrerReport(
            report=report,
            total=MoneyDTO(
                amount=total_amount,
                currency=query.convert_to,
            ),
        )
