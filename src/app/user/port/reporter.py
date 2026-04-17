from abc import ABC, abstractmethod

from app.user.dto.report import UserProfileReport
from domain.user.value_object import UserId


class UserReporter(ABC):
    @abstractmethod
    async def report_profile(
        self, target_user_id: UserId
    ) -> UserProfileReport | None:
        raise NotImplementedError
