from enum import StrEnum
from types import MappingProxyType
from typing import override

ROLE_HIERARCHY: MappingProxyType[str, int] = MappingProxyType(
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

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserRole):
            return NotImplemented

        return self.level == other.level

    @override
    def __hash__(self) -> int:
        return hash(self.value)

    @override
    def __ne__(self, other: object) -> bool:
        if not isinstance(other, UserRole):
            return NotImplemented

        return self.level != other.level

    @override
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, UserRole):
            return NotImplemented

        return self.level > other.level

    @override
    def __ge__(self, other: object) -> bool:
        if not isinstance(other, UserRole):
            return NotImplemented

        return self.level >= other.level

    @override
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, UserRole):
            return NotImplemented

        return self.level < other.level

    @override
    def __le__(self, other: object) -> bool:
        if not isinstance(other, UserRole):
            return NotImplemented

        return self.level <= other.level
