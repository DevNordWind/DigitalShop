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
from dishka import Provider, Scope, provide_all


class CategoryHandlersProvider(Provider):
    scope = Scope.REQUEST

    commands = provide_all(
        CreateCategory,
        ChangeCategoryNameDefaultLang,
        ChangeCategoryDescriptionDefaultLang,
        SetCategoryName,
        SetCategoryDescription,
        SetCategoryMedia,
        RemoveCategoryName,
        RemoveCategoryDescription,
        DeleteCategoryMedia,
        ArchiveCategory,
        RecoverCategory,
        TranslateCategoryNameToOthers,
        TranslateCategoryDescriptionToOthers,
        DeleteCategory,
        DeleteAllCategories,
        ArchiveAllCategories,
    )

    queries = provide_all(
        ListCategories,
        GetCategory,
        ListShortCategories,
        GetCategoryShort,
        GetCategoryWithGoodsAmount,
    )
