from dataclasses import dataclass, field

from domain.user.enums import UserRole
from presentation.aiogram.setting.general.exception import (
    CannotExcludeTechWorkForUsers,
)


@dataclass
class TechWorkSettings:
    status: bool = True
    exclude_for: set[UserRole] = field(
        default_factory=lambda: {UserRole.ADMIN, UserRole.SUPER_ADMIN},
    )

    def __post_init__(self) -> None:
        if UserRole.USER in self.exclude_for:
            raise CannotExcludeTechWorkForUsers


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


@dataclass(kw_only=True)
class GeneralBotSettings:
    tech_work: TechWorkSettings
    support: SupportContact | None
