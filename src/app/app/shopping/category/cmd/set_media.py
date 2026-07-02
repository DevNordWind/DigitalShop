from dataclasses import dataclass
from uuid import UUID

from app.app.common.dto.file_key import FileKeyRawDTO, FileKeyRawMapper
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.file_storage import File, FileStorageSession
from app.app.common.port.session import DatabaseSession
from app.domain.common.port import Clock
from app.domain.shopping.category.entity import Category
from app.domain.shopping.category.exception import CategoryNotFoundError
from app.domain.shopping.category.factory import CategoryMediaKeyFactory
from app.domain.shopping.category.port import CategoryRepository
from app.domain.shopping.category.service import CategoryAccessService
from app.domain.shopping.category.value_object import CategoryId, CategoryMediaKey


@dataclass(slots=True, frozen=True)
class SetCategoryMediaCmd:
    id: UUID
    media: FileKeyRawDTO


class SetCategoryMedia:
    def __init__(
        self,
        repository: CategoryRepository,
        actor_provider: ActorProvider,
        session: DatabaseSession,
        clock: Clock,
        media_key_factory: CategoryMediaKeyFactory,
        file_session: FileStorageSession,
    ):
        self._repository = repository
        self._actor_provider = actor_provider
        self._session = session
        self._clock = clock
        self._media_key_factory = media_key_factory
        self._file_session = file_session

    async def __call__(self, cmd: SetCategoryMediaCmd) -> None:
        CategoryAccessService.ensure_can_edit(actor=await self._actor_provider.get())

        category: Category | None = await self._repository.get(
            category_id=CategoryId(cmd.id),
        )
        if not category:
            raise CategoryNotFoundError

        old_media: CategoryMediaKey | None = category.media

        new_media: CategoryMediaKey = self._media_key_factory.generate(
            raw=FileKeyRawMapper.to_value_object(src=cmd.media),
            category_id=category.id,
        )
        if old_media:
            await self._file_session.delete(old_media)

        await self._file_session.put(
            file=File(key=new_media, content=cmd.media.content)
        )
        await self._file_session.commit()

        category.set_media(media=new_media, now=self._clock.now())

        await self._session.commit()
