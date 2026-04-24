from .get_award import GetReferralAward, GetReferralAwardQuery
from .get_coefficient import GetReferralCoefficient
from .get_my_awards import GetMyReferralAwards, GetMyReferralAwardsQuery
from .get_my_profile import GetMyReferrerProfile
from .get_my_report import GetMyReferrerReport, GetMyReferrerReportQuery

__all__ = (
    "GetMyReferralAwards",
    "GetMyReferralAwardsQuery",
    "GetMyReferrerProfile",
    "GetMyReferrerReport",
    "GetMyReferrerReportQuery",
    "GetReferralAward",
    "GetReferralAwardQuery",
    "GetReferralCoefficient",
)
