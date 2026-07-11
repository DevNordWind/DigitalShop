from datetime import datetime

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.port import Clock
from app.domain.shopping.category.entity import Category
from app.domain.shopping.category.enums import CategoryStatus
from app.domain.shopping.category.port import CategoryRepository
from app.domain.shopping.category.service import CategoryAccessService
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.enums import PositionStatus
from app.domain.shopping.position.port import PositionRepository


class ArchiveAllCategories:
    def __init__(
        self,
        category_repo: CategoryRepository,
        position_repo: PositionRepository,
        actor_provider: ActorProvider,
        session: DatabaseSession,
        clock: Clock,
    ):
        self._category_repo = category_repo
        self._position_repo = position_repo
        self._actor_provider = actor_provider
        self._session = session
        self._clock = clock

    async def __call__(self) -> None:
        CategoryAccessService.ensure_can_archive(actor=await self._actor_provider.get())

        categories: list[Category] = await self._category_repo.acquire_all_by_status(
            status=CategoryStatus.AVAILABLE,
        )
        now: datetime = self._clock.now()
        positions: list[
            Position
        ] = await self._position_repo.get_by_category_ids_status(
            category_ids=[c.id for c in categories],
            status=PositionStatus.AVAILABLE,
        )

        for category in categories:
            category.archive(now)

        for position in positions:
            position.archive(now=now)

        await self._session.commit()
