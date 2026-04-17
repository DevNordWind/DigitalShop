from typing import Protocol

from domain.user.entity import User
from domain.user.value_object import UserId


class UserRepository(Protocol):
    async def add(self, user: User) -> None:
        raise NotImplementedError

    async def get(self, user_id: UserId) -> User | None:
        raise NotImplementedError
