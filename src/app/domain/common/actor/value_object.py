from dataclasses import dataclass

from app.domain.user.enums import UserRole
from app.domain.user.value_object import UserId


@dataclass(slots=True, frozen=True)
class UserActor:
    id: UserId
    role: UserRole


@dataclass(slots=True, frozen=True)
class SystemActor:
    service_name: str


type Actor = UserActor | SystemActor
