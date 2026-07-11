from dishka import Provider, Scope, provide, provide_all

from app.app.referral.cmd import (
    ChangeReferrerProfileAwardCurrency,
    CreateReferralAwardFromOrder,
    CreateReferrerProfile,
    SetReferralCoefficient,
    SwitchReferrerProfileNotifications,
)
from app.app.referral.port import ReferralAwardReader, ReferralSystemReporter
from app.app.referral.query import (
    GetReferralAward,
    GetReferralCoefficient,
    GetReferrerProfile,
    GetReferrerReport,
    ListReferralAwards,
)
from app.domain.referral.port import (
    ReferralAwardRepository,
    ReferralPolicyRepository,
    ReferrerProfileRepository,
)
from app.domain.referral.service import (
    ReferralAwardDomainService,
    ReferrerProfileDomainService,
)
from app.infra.referral import (
    SqlAReferralAwardReader,
    SqlAReferralAwardRepository,
    SqlAReferralPolicyRepository,
    SqlAReferralSystemReporter,
    SqlAReferrerProfileRepository,
)


class ReferralDomainServicesProvider(Provider):
    scope = Scope.APP

    services = provide_all(
        ReferralAwardDomainService,
        ReferrerProfileDomainService,
    )


class ReferralHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        ChangeReferrerProfileAwardCurrency,
        CreateReferralAwardFromOrder,
        CreateReferrerProfile,
        SetReferralCoefficient,
        SwitchReferrerProfileNotifications,
    )

    queries = provide_all(
        GetReferralAward,
        GetReferralCoefficient,
        GetReferrerProfile,
        GetReferrerReport,
        ListReferralAwards,
    )


class ReferralAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repositories = provide_all(
        provide(SqlAReferralAwardRepository, provides=ReferralAwardRepository),
        provide(SqlAReferralPolicyRepository, provides=ReferralPolicyRepository),
        provide(SqlAReferrerProfileRepository, provides=ReferrerProfileRepository),
    )

    reader = provide(SqlAReferralAwardReader, provides=ReferralAwardReader)

    reporter = provide(SqlAReferralSystemReporter, provides=ReferralSystemReporter)
