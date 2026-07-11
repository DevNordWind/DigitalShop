from abc import ABC, abstractmethod

from app.domain.user.entity import User
from app.domain.user.value_object import UserId


class UserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, user_id: UserId) -> User | None:
        raise NotImplementedError
