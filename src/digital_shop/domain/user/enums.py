from enum import StrEnum

from frozendict import frozendict

ROLE_HIERARCHY: frozendict[str, int] = frozendict(
    {
        "USER": 0,
        "ADMIN": 1,
        "SUPER_ADMIN": 2,
    }
)


class UserRole(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

    @property
    def level(self) -> int:
        return ROLE_HIERARCHY[self.value]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserRole):
            return NotImplemented

        return self.level == other.level

    def __hash__(self) -> int:
        return hash(self.value)

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, UserRole):
            return NotImplemented

        return self.level != other.level

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, UserRole):
            return NotImplemented

        return self.level > other.level

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, UserRole):
            return NotImplemented

        return self.level >= other.level

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, UserRole):
            return NotImplemented

        return self.level < other.level

    def __le__(self, other: object) -> bool:
        if not isinstance(other, UserRole):
            return NotImplemented

        return self.level <= other.level
