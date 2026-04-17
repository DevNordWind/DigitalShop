from dishka import Provider, Scope, provide, provide_all

from app.referral.cmd import (
    ChangeReferrerProfileAwardCurrency,
    CreateReferralAwardFromOrder,
    CreateReferrerProfile,
    SetReferralCoefficient,
    SwitchReferrerProfileNotifications,
)
from app.referral.query import (
    GetMyReferralAwards,
    GetMyReferrerProfile,
    GetMyReferrerReport,
    GetReferralAward,
    GetReferralCoefficient,
)


class ReferralHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        provide(ChangeReferrerProfileAwardCurrency),
        provide(CreateReferralAwardFromOrder),
        provide(CreateReferrerProfile),
        provide(SwitchReferrerProfileNotifications),
        provide(SetReferralCoefficient),
    )

    queries = provide_all(
        GetMyReferralAwards,
        GetReferralCoefficient,
        GetMyReferrerReport,
        GetReferralAward,
        GetMyReferrerProfile,
    )
