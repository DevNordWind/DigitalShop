from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.session import DatabaseSession
from app.domain.common.port import Clock
from app.domain.shopping.category.entity import Category
from app.domain.shopping.category.exception import CategoryNotFoundError
from app.domain.shopping.category.port import CategoryRepository
from app.domain.shopping.category.service import CategoryAccessService
from app.domain.shopping.category.value_object import CategoryId
from app.domain.shopping.position.entity import Position
from app.domain.shopping.position.enums import PositionStatus
from app.domain.shopping.position.port import PositionRepository


@dataclass(slots=True, frozen=True)
class ArchiveCategoryCmd:
    id: UUID


class ArchiveCategory:
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

    async def __call__(self, cmd: ArchiveCategoryCmd) -> None:
        CategoryAccessService.ensure_can_archive(actor=await self._actor_provider.get())

        category: Category | None = await self._category_repo.acquire(
            category_id=CategoryId(cmd.id),
        )
        if not category:
            raise CategoryNotFoundError

        now: datetime = self._clock.now()

        category.archive(now=now)
        positions: list[
            Position
        ] = await self._position_repo.get_by_category_ids_status(
            category_ids=[category.id],
            status=PositionStatus.AVAILABLE,
        )
        for position in positions:
            position.archive(now)

        await self._session.commit()
