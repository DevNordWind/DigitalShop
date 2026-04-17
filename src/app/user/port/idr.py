from abc import ABC, abstractmethod
from uuid import UUID

from domain.user.value_object import UserId


class UserIdentifyResolver(ABC):
    @abstractmethod
    async def resolve(self, identifier: str | UUID) -> UserId | None:
        raise NotImplementedError
