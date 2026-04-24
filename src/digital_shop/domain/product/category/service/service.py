from domain.common.file import FileKeyRaw
from domain.common.port import Clock, UUIDProvider
from domain.product.category.entity import Category
from domain.product.category.exception import CategoryAccessDenied
from domain.product.category.service import CategoryMediaKeyFactory
from domain.product.category.service.access import CategoryAccessService
from domain.product.category.value_object import (
    CategoryDescription,
    CategoryId,
    CategoryName,
)
from domain.user.entity import User


class CategoryService:
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
        creator: User,
        name: CategoryName,
        description: CategoryDescription | None,
        media_raw: FileKeyRaw | None,
    ) -> Category:
        if not CategoryAccessService.can_create(creator=creator):
            raise CategoryAccessDenied

        category_id = CategoryId(self._uuid())
        media_key = None

        if media_raw is not None:
            media_key = self._media_key_factory.generate(
                raw=media_raw,
                category_id=category_id,
            )

        return Category(
            id=category_id,
            creator_id=creator.id,
            name=name,
            description=description,
            media=media_key,
            created_at=self._clock.now(),
            updated_at=None,
            archived_at=None,
        )
