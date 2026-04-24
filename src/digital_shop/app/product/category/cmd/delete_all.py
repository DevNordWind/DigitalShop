from app.common.port import DatabaseSession, FileStorageSession
from app.user.service import GetCurrentUser
from domain.common.port import Clock
from domain.product.category.entity import Category
from domain.product.category.enums import CategoryStatus
from domain.product.category.exception import CategoryAccessDenied
from domain.product.category.port import CategoryRepository
from domain.product.category.service import CategoryAccessService
from domain.product.position.entity import Position
from domain.product.position.port import PositionRepository
from domain.user.entity import User


class DeleteAllCategories:
    def __init__(
        self,
        category_repo: CategoryRepository,
        position_repo: PositionRepository,
        current_user: GetCurrentUser,
        file_session: FileStorageSession,
        session: DatabaseSession,
        clock: Clock,
    ):
        self._category_repo: CategoryRepository = category_repo
        self._position_repo: PositionRepository = position_repo
        self._current_user: GetCurrentUser = current_user
        self._file_session: FileStorageSession = file_session
        self._session: DatabaseSession = session
        self._clock: Clock = clock

    async def __call__(self) -> None:
        deleter: User = await self._current_user()

        if not CategoryAccessService.can_delete(deleter=deleter):
            raise CategoryAccessDenied

        categories: list[Category] = await self._category_repo.get_all(
            status=CategoryStatus.ARCHIVED,
        )
        positions: list[
            Position
        ] = await self._position_repo.get_by_category_ids_for_update(
            category_ids=[c.id for c in categories],
            status=None,
        )
        for category in categories:
            category.ensure_deletable()
            if category.media:
                await self._file_session.delete(category.media)
            await self._category_repo.delete(category=category)

        for position in positions:
            for media_key in position.media:
                await self._file_session.delete(media_key)

        await self._session.commit()
