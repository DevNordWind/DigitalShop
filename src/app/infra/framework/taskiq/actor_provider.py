from typing import override

from app.app.common.port.actor_provider import ActorProvider
from app.domain.common.actor import Actor, SystemActor


class TaskIqActorProvider(ActorProvider):
    @override
    async def get(self) -> Actor:
        return SystemActor(service_name="TaskIq")
