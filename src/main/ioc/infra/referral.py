from dishka import Provider, Scope, provide, provide_all

from app.referral.port import ReferralAwardReader, ReferralSystemReporter
from domain.referral.port import (
    ReferralAwardRepository,
    ReferralPolicyRepository,
)
from domain.referral.port.profile_repository import ReferrerProfileRepository
from infra.referral.award_repository import ReferralAwardRepositoryImpl
from infra.referral.policy_repository import ReferralPolicyRepositoryImpl
from infra.referral.profile_repository import ReferrerProfileRepositoryImpl
from infra.referral.reader.reader import ReferralAwardReaderImpl
from infra.referral.reporter.reporter import ReferralSystemReporterImpl


class ReferralAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repositories = provide_all(
        provide(ReferralAwardRepositoryImpl, provides=ReferralAwardRepository),
        provide(
            ReferralPolicyRepositoryImpl,
            provides=ReferralPolicyRepository,
        ),
        provide(
            ReferrerProfileRepositoryImpl,
            provides=ReferrerProfileRepository,
        ),
    )

    reader = provide(ReferralAwardReaderImpl, provides=ReferralAwardReader)

    reporter = provide(
        ReferralSystemReporterImpl,
        provides=ReferralSystemReporter,
    )
