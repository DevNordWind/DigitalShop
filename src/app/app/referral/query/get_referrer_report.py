from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.money import MoneyMapper
from app.app.common.port.actor_provider import ActorProvider
from app.app.referral.dto.report import ConvertedReferrerReport, ReferrerReport
from app.app.referral.port import ReferralSystemReporter
from app.domain.common.exchange_rate import (
    CurrencyPair,
    ExchangeRate,
    ExchangeRateGateway,
)
from app.domain.common.exchange_rate.service import MoneyConverter
from app.domain.common.money import Currency, Money
from app.domain.common.time_period import TimePeriod
from app.domain.referral.service import ReferralAwardAccessService
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class GetReferrerReportQuery:
    target_user_id: UUID

    convert_to: Currency
    period: TimePeriod | None


class GetReferrerReport:
    def __init__(
        self,
        reporter: ReferralSystemReporter,
        rate_gw: ExchangeRateGateway,
        actor_provider: ActorProvider,
    ):
        self._reporter: ReferralSystemReporter = reporter
        self._rate_gw: ExchangeRateGateway = rate_gw
        self._actor_provider = actor_provider

    async def __call__(
        self,
        query: GetReferrerReportQuery,
    ) -> ConvertedReferrerReport:
        referrer_id: UserId = UserId(query.target_user_id)

        ReferralAwardAccessService.ensure_can_view(
            actor=await self._actor_provider.get(), referrer_id=referrer_id
        )

        report: ReferrerReport = await self._reporter.get_referrer_report(
            period=query.period, referrer_id=referrer_id
        )

        pairs: list[CurrencyPair] = [
            CurrencyPair(source=currency, target=query.convert_to)
            for currency in report.awards_sum
            if currency != query.convert_to
        ]
        rates: tuple[ExchangeRate, ...] = await self._rate_gw.get_many(pairs=pairs)
        converted: Money = MoneyConverter.convert_many(
            amounts={
                currency: MoneyMapper.to_value_object(src=amount)
                for currency, amount in report.awards_sum.items()
            },
            rates=rates,
            target=query.convert_to,
        )

        return ConvertedReferrerReport(
            report=report, total=MoneyMapper.to_dto(src=converted)
        )
