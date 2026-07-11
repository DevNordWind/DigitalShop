from typing import Final, override

from app.app.common.port.actor_provider import ActorProvider
from app.domain.common.actor import Actor, SystemActor

_ACTOR: Final[SystemActor] = SystemActor(service_name="FastAPI")


class FastAPIActorProvider(ActorProvider):
    @override
    async def get(self) -> Actor:
        return _ACTOR
