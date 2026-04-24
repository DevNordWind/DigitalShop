from dataclasses import dataclass
from uuid import UUID

from app.common.dto.file_key import FileKeyRawDTO, FileKeyRawMapper
from app.common.port import DatabaseSession
from app.common.port.file_storage import FileStorageSession
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
class SetCategoryMediaCmd:
    id: UUID
    media: FileKeyRawDTO


class SetCategoryMedia:
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

    async def __call__(self, cmd: SetCategoryMediaCmd) -> None:
        editor: User = await self._current_user()

        if not CategoryAccessService.can_edit(editor=editor):
            raise CategoryAccessDenied

        category: Category | None = await self._repository.get(
            category_id=CategoryId(cmd.id),
        )
        if not category:
            raise CategoryNotFound

        old_media: CategoryMediaKey | None = category.media

        new_media: CategoryMediaKey = self._media_key_factory.generate(
            raw=FileKeyRawMapper.to_value_object(src=cmd.media),
            category_id=category.id,
        )
        if old_media:
            await self._file_session.delete(old_media)
        await self._file_session.put(new_media, content=cmd.media.content)
        await self._file_session.commit()

        category.set_media(media=new_media, now=self._clock.now())

        await self._session.commit()
