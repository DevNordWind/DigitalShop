from abc import ABC, abstractmethod

from domain.user.enums import UserRole
from domain.user.value_object import UserId


class UserIdentifyProvider(ABC):
    @abstractmethod
    async def get_user_id(self) -> UserId:
        raise NotImplementedError

    @abstractmethod
    async def get_role(self) -> UserRole:
        raise NotImplementedError
