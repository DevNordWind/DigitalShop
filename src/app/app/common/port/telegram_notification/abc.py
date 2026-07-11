from abc import ABC, abstractmethod
from typing import Any

from app.app.common.port.telegram_notification.dto import NotificationRequest
from app.domain.user.value_object import UserId


class TelegramNotification(ABC):
    @abstractmethod
    async def send(
        self,
        user_id: UserId,
        request: NotificationRequest,
        **kwargs: Any,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def send_admins(
        self,
        request: NotificationRequest,
        **kwargs: Any,
    ) -> None:
        raise NotImplementedError
