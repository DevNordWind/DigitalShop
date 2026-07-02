from dataclasses import dataclass
from uuid import UUID

from app.app.common.port.actor_provider import ActorProvider
from app.app.shopping.category.dto.category import (
    CategoryWithGoodsAmountDTO,
)
from app.app.shopping.category.port import CategoryReader
from app.domain.shopping.category.exception import CategoryNotFoundError
from app.domain.shopping.category.service import CategoryAccessService
from app.domain.shopping.category.value_object import CategoryId


@dataclass(slots=True, frozen=True)
class GetCategoryWithGoodsAmountQuery:
    id: UUID


class GetCategoryWithGoodsAmount:
    def __init__(self, reader: CategoryReader, actor_provider: ActorProvider):
        self._reader = reader
        self._actor_provider = actor_provider

    async def __call__(
        self, query: GetCategoryWithGoodsAmountQuery
    ) -> CategoryWithGoodsAmountDTO:
        category: (
            CategoryWithGoodsAmountDTO | None
        ) = await self._reader.read_with_goods_amount(
            category_id=CategoryId(value=query.id),
        )
        if not category:
            raise CategoryNotFoundError

        CategoryAccessService.ensure_can_view(
            actor=await self._actor_provider.get(),
            category_status=category.category.status,
        )

        return category
