from abc import ABC, abstractmethod

from app.domain.common.actor import Actor


class ActorProvider(ABC):
    @abstractmethod
    async def get(self) -> Actor:
        raise NotImplementedError
