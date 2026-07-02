from dataclasses import dataclass

from app.app.common.dto.file_key import FileKeyRawDTO, FileKeyRawMapper
from app.app.common.dto.localized import LocalizedTextDTO
from app.app.common.port.actor_provider import ActorProvider
from app.app.common.port.file_storage import File, FileStorageSession
from app.app.common.port.session import DatabaseSession
from app.app.shopping.category.dto.description import CategoryDescriptionMapper
from app.app.shopping.category.dto.name import CategoryNameMapper
from app.domain.common.actor import UserActor
from app.domain.common.file_key import FileKeyRaw
from app.domain.shopping.category.entity import Category
from app.domain.shopping.category.port import CategoryRepository
from app.domain.shopping.category.service import (
    CategoryAccessService,
    CategoryDomainService,
)
from app.domain.shopping.category.value_object import (
    CategoryDescription,
    CategoryId,
    CategoryMediaKey,
)


@dataclass(slots=True, frozen=True)
class CreateCategoryCmd:
    name: LocalizedTextDTO
    description: LocalizedTextDTO | None
    media: FileKeyRawDTO | None


class CreateCategory:
    def __init__(
        self,
        repo: CategoryRepository,
        actor_provider: ActorProvider,
        service: CategoryDomainService,
        file_session: FileStorageSession,
        session: DatabaseSession,
    ):
        self._repo = repo
        self._actor_provider = actor_provider
        self._service = service
        self._file_session = file_session
        self._session = session

    async def __call__(self, cmd: CreateCategoryCmd) -> CategoryId:
        name = CategoryNameMapper.to_value_object(src=cmd.name)
        description: CategoryDescription | None = None
        media: FileKeyRaw | None = None

        if cmd.description:
            description = CategoryDescriptionMapper.to_value_object(
                src=cmd.description,
            )

        if cmd.media:
            media = FileKeyRawMapper.to_value_object(src=cmd.media)

        actor: UserActor = CategoryAccessService.ensure_can_create(
            actor=await self._actor_provider.get()
        )

        category: Category = self._service.create(
            creator_id=actor.id,
            name=name,
            description=description,
            media_raw=media,
        )

        category_id = category.id
        media_key: CategoryMediaKey | None = category.media

        if media_key is not None and cmd.media is not None:
            await self._file_session.put(
                file=File(content=cmd.media.content, key=media_key)
            )
            await self._file_session.commit()

        await self._repo.add(category)
        await self._session.commit()

        return category_id
