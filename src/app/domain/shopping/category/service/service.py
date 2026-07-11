from app.domain.common.file_key import FileKeyRaw
from app.domain.common.port import Clock, UUIDProvider
from app.domain.shopping.category.entity import Category
from app.domain.shopping.category.factory import CategoryMediaKeyFactory
from app.domain.shopping.category.value_object import (
    CategoryDescription,
    CategoryId,
    CategoryMediaKey,
    CategoryName,
)
from app.domain.user.value_object import UserId


class CategoryDomainService:
    def __init__(
        self,
        clock: Clock,
        uuid: UUIDProvider,
        media_key_factory: CategoryMediaKeyFactory,
    ):
        self._clock: Clock = clock
        self._uuid: UUIDProvider = uuid
        self._media_key_factory: CategoryMediaKeyFactory = media_key_factory

    def create(
        self,
        creator_id: UserId,
        name: CategoryName,
        description: CategoryDescription | None,
        media_raw: FileKeyRaw | None,
    ) -> Category:
        category_id = CategoryId(self._uuid())
        media_key: CategoryMediaKey | None = None

        if media_raw is not None:
            media_key = self._media_key_factory.generate(
                raw=media_raw,
                category_id=category_id,
            )

        return Category(
            id=category_id,
            creator_id=creator_id,
            name=name,
            description=description,
            media=media_key,
            created_at=self._clock.now(),
            updated_at=None,
            archived_at=None,
        )
