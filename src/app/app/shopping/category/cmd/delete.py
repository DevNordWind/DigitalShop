from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.file_storage import FileStorageSession
from app.app.common.port.session import DatabaseSession
from app.domain.common.port import Clock
from app.domain.shopping.category.entity import Category
from app.domain.shopping.category.exception import CategoryNotFoundError
from app.domain.shopping.category.port import CategoryRepository
from app.domain.shopping.category.service import CategoryAccessService
from app.domain.shopping.category.value_object import CategoryId
from app.domain.shopping.position.port import PositionRepository


@dataclass(slots=True, frozen=True)
class DeleteCategoryCmd:
    id: UUID


class DeleteCategory:
    def __init__(
        self,
        category_repo: CategoryRepository,
        position_repo: PositionRepository,
        actor_provider: ActorProvider,
        file_session: FileStorageSession,
        session: DatabaseSession,
        clock: Clock,
    ):
        self._category_repo = category_repo
        self._position_repo = position_repo
        self._actor_provider = actor_provider
        self._file_session = file_session
        self._session = session
        self._clock = clock

    async def __call__(self, cmd: DeleteCategoryCmd) -> None:
        CategoryAccessService.ensure_can_delete(actor=await self._actor_provider.get())

        category: Category | None = await self._category_repo.acquire(
            category_id=CategoryId(cmd.id),
        )
        if not category:
            raise CategoryNotFoundError

        category.ensure_deletable()
        await self._category_repo.delete(category)
        if category.media:
            await self._file_session.delete(category.media)

        positions = await self._position_repo.get_by_category_ids_status(
            category_ids=[category.id],
            status=None,
        )
        for position in positions:
            for media_key in position.media:
                await self._file_session.delete(media_key)

        await self._session.commit()

        await self._file_session.commit()
