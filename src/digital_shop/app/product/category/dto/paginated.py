from dataclasses import dataclass

from app.product.category.dto.category import CategoryDTO, CategoryShortDTO


@dataclass(slots=True, frozen=True)
class CategoriesPaginated:
    categories: list[CategoryDTO]
    total: int


@dataclass(slots=True, frozen=True)
class CategoriesShortPaginated:
    categories: list[CategoryShortDTO]
    total: int
