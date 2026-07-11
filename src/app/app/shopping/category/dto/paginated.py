from dataclasses import dataclass

from app.app.shopping.category.dto.category import CategoryDTO, CategoryShortDTO


@dataclass(slots=True, frozen=True)
class CategoriesPaginated:
    categories: list[CategoryDTO]
    total: int


@dataclass(slots=True, frozen=True)
class CategoriesShortPaginated:
    categories: list[CategoryShortDTO]
    total: int
