from abc import ABC, abstractmethod

from app.app.user.dto import UserProfileDTO
from app.domain.user.value_object import UserId


class UserReader(ABC):
    @abstractmethod
    async def read_profile(self, user_id: UserId) -> UserProfileDTO | None:
        raise NotImplementedError
