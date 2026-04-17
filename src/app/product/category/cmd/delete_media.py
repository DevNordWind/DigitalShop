from contextlib import suppress
from dataclasses import dataclass
from uuid import UUID

from app.common.port import DatabaseSession
from app.common.port.file_storage import FileStorageError, FileStorageSession
from app.product.category.exception import CategoryNotFound
from app.user.service import GetCurrentUser
from domain.common.port import Clock
from domain.product.category.entity import Category
from domain.product.category.exception import CategoryAccessDenied
from domain.product.category.port import CategoryRepository
from domain.product.category.service import (
    CategoryAccessService,
    CategoryMediaKeyFactory,
)
from domain.product.category.value_object import CategoryId, CategoryMediaKey
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class DeleteCategoryMediaCmd:
    id: UUID


class DeleteCategoryMedia:
    def __init__(
        self,
        repository: CategoryRepository,
        current_user: GetCurrentUser,
        session: DatabaseSession,
        clock: Clock,
        media_key_factory: CategoryMediaKeyFactory,
        file_session: FileStorageSession,
    ):
        self._repository: CategoryRepository = repository
        self._current_user: GetCurrentUser = current_user
        self._session: DatabaseSession = session
        self._clock: Clock = clock
        self._media_key_factory: CategoryMediaKeyFactory = media_key_factory
        self._file_session: FileStorageSession = file_session

    async def __call__(self, cmd: DeleteCategoryMediaCmd) -> None:
        editor: User = await self._current_user()

        if not CategoryAccessService.can_edit(editor=editor):
            raise CategoryAccessDenied

        category: Category | None = await self._repository.get(
            category_id=CategoryId(cmd.id),
        )
        if not category:
            raise CategoryNotFound

        media: CategoryMediaKey | None = category.media

        category.delete_media(now=self._clock.now())

        await self._session.commit()

        with suppress(FileStorageError):
            if media is not None:
                await self._file_session.delete(media)
                await self._file_session.commit()
