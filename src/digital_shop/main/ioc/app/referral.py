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
from dishka import Provider, Scope, provide_all


class ReferralHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        ChangeReferrerProfileAwardCurrency,
        CreateReferralAwardFromOrder,
        CreateReferrerProfile,
        SwitchReferrerProfileNotifications,
        SetReferralCoefficient,
    )

    queries = provide_all(
        GetMyReferralAwards,
        GetReferralCoefficient,
        GetMyReferrerReport,
        GetReferralAward,
        GetMyReferrerProfile,
    )
