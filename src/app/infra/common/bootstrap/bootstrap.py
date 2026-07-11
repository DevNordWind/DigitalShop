from app.infra.common.bootstrap.entities import DefaultEntitiesBootstrap
from app.infra.common.bootstrap.infrastructure import InfrastructureBootstrap


class Bootstrap:
    def __init__(
        self,
        infrastructure: InfrastructureBootstrap,
        entities: DefaultEntitiesBootstrap,
    ):
        self._infrastructure = infrastructure
        self._entities = entities

    async def startup(self) -> None:
        await self._infrastructure.startup()
        await self._entities.startup()
