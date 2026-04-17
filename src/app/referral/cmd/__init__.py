from .change_award_currency import (
    ChangeReferrerProfileAwardCurrency,
    ChangeReferrerProfileAwardCurrencyCmd,
)
from .create_from_order import (
    CreateReferralAwardFromOrder,
    CreateReferralAwardFromOrderCmd,
)
from .create_profile import CreateReferrerProfile, CreateReferrerProfileCmd
from .set_referral_coefficient import (
    SetReferralCoefficient,
    SetReferralCoefficientCmd,
)
from .switch_send_notifications import SwitchReferrerProfileNotifications

__all__ = (
    "ChangeReferrerProfileAwardCurrency",
    "ChangeReferrerProfileAwardCurrencyCmd",
    "CreateReferralAwardFromOrder",
    "CreateReferralAwardFromOrderCmd",
    "CreateReferrerProfile",
    "CreateReferrerProfileCmd",
    "SetReferralCoefficient",
    "SetReferralCoefficientCmd",
    "SwitchReferrerProfileNotifications",
)
