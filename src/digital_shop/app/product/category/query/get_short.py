from dataclasses import dataclass
from uuid import UUID

from app.product.category.dto.category import CategoryShortDTO
from app.product.category.exception import CategoryNotFound
from app.product.category.port import CategoryReader
from app.user.port import UserIdentifyProvider
from domain.product.category.enums import CategoryStatus
from domain.product.category.exception import CategoryAccessDenied
from domain.product.category.service import CategoryAccessService
from domain.product.category.value_object import CategoryId


@dataclass(slots=True, frozen=True)
class GetCategoryShortQuery:
    id: UUID


class GetCategoryShort:
    def __init__(self, reader: CategoryReader, idp: UserIdentifyProvider):
        self._reader: CategoryReader = reader
        self._idp: UserIdentifyProvider = idp

    async def __call__(self, query: GetCategoryShortQuery) -> CategoryShortDTO:
        category: CategoryShortDTO | None = await self._reader.read_short(
            category_id=CategoryId(value=query.id),
        )
        if not category:
            raise CategoryNotFound

        if (
            category.status == CategoryStatus.ARCHIVED
            and not CategoryAccessService.can_view_archived(
                viewer_role=await self._idp.get_role(),
            )
        ):
            raise CategoryAccessDenied

        return category
