from abc import ABC, abstractmethod

from app.domain.shopping.category.entity import Category
from app.domain.shopping.category.enums import CategoryStatus
from app.domain.shopping.category.value_object import CategoryId


class CategoryRepository(ABC):
    @abstractmethod
    async def add(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, category_id: CategoryId) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_status(
        self,
        status: CategoryStatus | None = None,
    ) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    async def acquire(self, category_id: CategoryId) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    async def acquire_all_by_status(
        self, status: CategoryStatus | None = None
    ) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, category: Category) -> None:
        raise NotImplementedError
