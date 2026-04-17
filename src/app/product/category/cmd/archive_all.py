from datetime import datetime

from app.common.port import DatabaseSession
from app.user.service import GetCurrentUser
from domain.common.port import Clock
from domain.product.category.entity import Category
from domain.product.category.enums import CategoryStatus
from domain.product.category.exception import CategoryAccessDenied
from domain.product.category.port import CategoryRepository
from domain.product.category.service import CategoryAccessService
from domain.product.position.entity import Position
from domain.product.position.enums import PositionStatus
from domain.product.position.port import PositionRepository
from domain.user.entity import User


class ArchiveAllCategories:
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

    async def __call__(self) -> None:
        archiver: User = await self._current_user()

        if not CategoryAccessService.can_archive(archiver=archiver):
            raise CategoryAccessDenied

        categories: list[Category] = await self._category_repo.get_all(
            status=CategoryStatus.AVAILABLE,
        )
        now: datetime = self._clock.now()
        positions: list[
            Position
        ] = await self._position_repo.get_by_category_ids_for_update(
            category_ids=[c.id for c in categories],
            status=PositionStatus.AVAILABLE,
        )

        for category in categories:
            category.archive(now)

        for position in positions:
            position.archive(now=now)

        await self._session.commit()
