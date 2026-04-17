from dishka import Provider, Scope, provide, provide_all

from app.product.category.cmd import (
    ArchiveAllCategories,
    ArchiveCategory,
    ChangeCategoryDescriptionDefaultLang,
    ChangeCategoryNameDefaultLang,
    CreateCategory,
    DeleteAllCategories,
    DeleteCategory,
    DeleteCategoryMedia,
    RecoverCategory,
    RemoveCategoryDescription,
    RemoveCategoryName,
    SetCategoryDescription,
    SetCategoryMedia,
    SetCategoryName,
    TranslateCategoryDescriptionToOthers,
    TranslateCategoryNameToOthers,
)
from app.product.category.query import (
    GetCategory,
    GetCategoryShort,
    GetCategoryWithGoodsAmount,
    ListCategories,
    ListShortCategories,
)


class CategoryHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        provide(CreateCategory),
        provide(ChangeCategoryNameDefaultLang),
        provide(ChangeCategoryDescriptionDefaultLang),
        provide(SetCategoryName),
        provide(SetCategoryDescription),
        provide(SetCategoryMedia),
        provide(RemoveCategoryName),
        provide(RemoveCategoryDescription),
        provide(DeleteCategoryMedia),
        provide(ArchiveCategory),
        provide(RecoverCategory),
        provide(TranslateCategoryNameToOthers),
        provide(TranslateCategoryDescriptionToOthers),
        provide(DeleteCategory),
        provide(DeleteAllCategories),
        provide(ArchiveAllCategories),
    )

    queries = provide_all(
        provide(ListCategories),
        provide(GetCategory),
        provide(ListShortCategories),
        provide(GetCategoryShort),
        provide(GetCategoryWithGoodsAmount),
    )
