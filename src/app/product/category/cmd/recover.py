from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.common.port import DatabaseSession
from app.product.category.exception import CategoryNotFound
from app.user.service import GetCurrentUser
from domain.common.port import Clock
from domain.product.category.entity import Category
from domain.product.category.exception import CategoryAccessDenied
from domain.product.category.port import CategoryRepository
from domain.product.category.service import CategoryAccessService
from domain.product.category.value_object import CategoryId
from domain.product.position.entity import Position
from domain.product.position.port import PositionRepository
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class RecoverCategoryCmd:
    id: UUID


class RecoverCategory:
    def __init__(
        self,
        category_repo: CategoryRepository,
        position_repo: PositionRepository,
        current_user: GetCurrentUser,
        session: DatabaseSession,
        clock: Clock,
    ):
        self._category_repo: CategoryRepository = category_repo
        self._position_repo: PositionRepository = position_repo
        self._current_user: GetCurrentUser = current_user
        self._session: DatabaseSession = session
        self._clock: Clock = clock

    async def __call__(self, cmd: RecoverCategoryCmd) -> None:
        recoverer: User = await self._current_user()

        if not CategoryAccessService.can_recover(recoverer=recoverer):
            raise CategoryAccessDenied

        category: Category | None = await self._category_repo.get(
            category_id=CategoryId(cmd.id),
        )
        if not category:
            raise CategoryNotFound

        now: datetime = self._clock.now()
        positions: list[
            Position
        ] = await self._position_repo.get_by_category_ids_for_update(
            category_ids=[category.id],
        )
        category.recover(now=now)
        for position in positions:
            position.recover(now=now)

        await self._session.commit()
