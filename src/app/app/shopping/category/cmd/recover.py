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


@dataclass(slots=True, frozen=True)
class RecoverCategoryCmd:
    id: UUID


class RecoverCategory:
    def __init__(
        self,
        category_repo: CategoryRepository,
        actor_provider: ActorProvider,
        session: DatabaseSession,
        clock: Clock,
    ):
        self._category_repo = category_repo
        self._actor_provider = actor_provider
        self._session = session
        self._clock = clock

    async def __call__(self, cmd: RecoverCategoryCmd) -> None:
        CategoryAccessService.ensure_can_recover(actor=await self._actor_provider.get())

        category: Category | None = await self._category_repo.get(
            category_id=CategoryId(cmd.id),
        )
        if not category:
            raise CategoryNotFoundError

        now: datetime = self._clock.now()
        category.recover(now=now)

        await self._session.commit()
