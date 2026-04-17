from dataclasses import dataclass
from datetime import datetime

from domain.common.money import Currency
from domain.user.value_object import UserId


@dataclass(kw_only=True)
class ReferrerProfile:
    user_id: UserId
    award_currency: Currency

    send_notifications: bool = True

    created_at: datetime

    def change_award_currency(self, new_currency: Currency) -> None:
        self.award_currency = new_currency

    def switch_send_notifictions(self) -> None:
        self.send_notifications = not self.send_notifications
