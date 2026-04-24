from dataclasses import dataclass
from datetime import datetime

from domain.user.enums import UserRole
from domain.user.value_object import UserId


@dataclass
class User:
    id: UserId
    referrer_id: UserId | None

    role: UserRole

    reg_at: datetime

    def assign_role(self, role: UserRole) -> None:
        if self.role == role:
            return

        self.role = role

    def system_assign_role(self, minimum_role: UserRole) -> UserRole:
        if self.role >= minimum_role:
            pass
        else:
            self.role = minimum_role

        return self.role
