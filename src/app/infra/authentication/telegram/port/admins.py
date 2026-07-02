from abc import abstractmethod
from typing import Protocol

from app.infra.authentication.telegram.model import TelegramId


class SuperAdminsProvider(Protocol):
    @abstractmethod
    async def get(self) -> set[TelegramId]:
        raise NotImplementedError
