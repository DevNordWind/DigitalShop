from abc import ABC, abstractmethod

from presentation.aiogram.port.broadcast.dto import BroadcastRequest


class TelegramBroadcaster(ABC):
    @abstractmethod
    async def broadcast(self, request: BroadcastRequest) -> None:
        raise NotImplementedError
