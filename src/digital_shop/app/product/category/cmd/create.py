from dataclasses import dataclass

from app.common.dto.file_key import FileKeyRawDTO, FileKeyRawMapper
from app.common.dto.localized import LocalizedTextDTO
from app.common.port import DatabaseSession
from app.common.port.file_storage import FileStorageSession
from app.product.category.dto.description import CategoryDescriptionMapper
from app.product.category.dto.name import CategoryNameMapper
from app.user.service import GetCurrentUser
from domain.common.file import FileKeyRaw
from domain.product.category.entity import Category
from domain.product.category.port import CategoryRepository
from domain.product.category.service import CategoryService
from domain.product.category.value_object import (
    CategoryDescription,
    CategoryId,
    CategoryMediaKey,
)
from domain.user.entity import User


@dataclass(slots=True, frozen=True)
class CreateCategoryCmd:
    name: LocalizedTextDTO
    description: LocalizedTextDTO | None
    media: FileKeyRawDTO | None


class CreateCategory:
    def __init__(
        self,
        repo: CategoryRepository,
        current_user: GetCurrentUser,
        service: CategoryService,
        file_session: FileStorageSession,
        session: DatabaseSession,
    ):
        self._repo: CategoryRepository = repo
        self._current_user: GetCurrentUser = current_user
        self._service: CategoryService = service
        self._file_session: FileStorageSession = file_session
        self._session: DatabaseSession = session

    async def __call__(self, cmd: CreateCategoryCmd) -> CategoryId:
        current_user: User = await self._current_user()

        name = CategoryNameMapper.to_value_object(src=cmd.name)
        description: CategoryDescription | None = None
        media: FileKeyRaw | None = None

        if cmd.description:
            description = CategoryDescriptionMapper.to_value_object(
                src=cmd.description,
            )

        if cmd.media:
            media = FileKeyRawMapper.to_value_object(src=cmd.media)

        category: Category = self._service.create(
            creator=current_user,
            name=name,
            description=description,
            media_raw=media,
        )

        category_id = category.id
        media_key: CategoryMediaKey | None = category.media

        if media_key is not None and cmd.media is not None:
            await self._file_session.put(
                key=media_key,
                content=cmd.media.content,
            )
            await self._file_session.commit()

        await self._repo.add(category)
        await self._session.commit()

        return category_id
