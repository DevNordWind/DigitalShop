from typing import Protocol

from domain.product.category.entity import Category
from domain.product.category.enums import CategoryStatus
from domain.product.category.value_object import CategoryId


class CategoryRepository(Protocol):
    async def add(self, category: Category) -> None:
        raise NotImplementedError

    async def get(self, category_id: CategoryId) -> Category | None:
        raise NotImplementedError

    async def get_all(
        self,
        status: CategoryStatus | None = None,
    ) -> list[Category]:
        raise NotImplementedError

    async def delete(self, category: Category) -> None:
        raise NotImplementedError
