from dataclasses import dataclass, field

from app.domain.user.enums import UserRole
from app.presentation.aiogram.setting.general.exception import (
    CannotExcludeTechWorkForUsersError,
)


@dataclass(slots=True)
class TechWorkSettings:
    status: bool = True
    exclude_for: set[UserRole] = field(
        default_factory=lambda: {UserRole.ADMIN, UserRole.SUPER_ADMIN},
    )

    def __post_init__(self) -> None:
        if UserRole.USER in self.exclude_for:
            raise CannotExcludeTechWorkForUsersError


@dataclass(slots=True)
class SupportContact:
    username: str

    def __post_init__(self) -> None:
        username = self.username

        if "t.me/" in username:
            username = username.split("/")[-1]
        self.username = username.strip("@")

    @property
    def url(self) -> str:
        return f"https://t.me/{self.username}"


@dataclass(slots=True, kw_only=True)
class GeneralBotSettings:
    tech_work: TechWorkSettings
    support: SupportContact | None

    def switch_tech_work_status(self) -> None:
        self.tech_work.status = not self.tech_work.status

    def set_support(self, support: SupportContact) -> None:
        self.support = support
