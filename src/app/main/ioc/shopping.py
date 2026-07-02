from dishka import Provider, Scope, provide, provide_all

from app.app.shopping.category.cmd import (
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
from app.app.shopping.category.port import CategoryReader
from app.app.shopping.category.query import (
    GetCategory,
    GetCategoryShort,
    GetCategoryWithGoodsAmount,
    ListCategories,
    ListShortCategories,
)
from app.app.shopping.position.cmd import (
    AddPositionItems,
    AddPositionMedia,
    ArchiveAllPositionItems,
    ArchiveAllPositionsByCategory,
    ArchivePosition,
    ArchivePositionItem,
    ChangePositionDescriptionDefaultLang,
    ChangePositionNameDefaultLang,
    ChangePositionPriceBaseCurrency,
    ConvertPositionPriceToOthers,
    CreatePosition,
    DeleteAllPositionItems,
    DeleteAllPositionsByCategory,
    DeletePosition,
    DeletePositionItem,
    RecoverPosition,
    RecoverPositionItem,
    RemovePositionDescription,
    RemovePositionMedia,
    SetPositionDescription,
    SetPositionName,
    SetPositionPrice,
    TranslatePositionDescriptionToOthers,
    TranslatePositionNameToOthers,
)
from app.app.shopping.position.port import PositionReader
from app.app.shopping.position.query import (
    GetPosition,
    GetPositionItem,
    GetPositionWithItemsAmount,
    ListPositionItems,
    ListPositionsByCategory,
    ListPositionsShortByCategory,
    ListPositionsWithItemsAmountByCategory,
)
from app.domain.shopping.category.factory import CategoryMediaKeyFactory
from app.domain.shopping.category.port import CategoryRepository
from app.domain.shopping.category.service import CategoryDomainService
from app.domain.shopping.position.factory import (
    FulfillmentStrategyFactory,
    PositionMediaKeyFactory,
    WarehouseFactory,
)
from app.domain.shopping.position.item.factory import FixedItemFactory, StockItemFactory
from app.domain.shopping.position.item.port import (
    FixedItemRepository,
    StockItemRepository,
)
from app.domain.shopping.position.port import PositionRepository
from app.domain.shopping.position.service import (
    PositionDomainService,
    PositionWarehouseDomainService,
)
from app.domain.shopping.position.service.fulfillment import (
    PositionFulfillmentDomainService,
)
from app.domain.shopping.position.strategy import (
    FixedFulfillment,
    FixedWarehouse,
    StockFulfillment,
    UnlimitedWarehouse,
)
from app.infra.shopping import (
    SqlACategoryReader,
    SqlACategoryRepository,
    SqlAFixedItemRepository,
    SqlAPositionRepository,
    SqlAStockItemRepository,
)
from app.infra.shopping.position import (
    DishkaFulfillmentStrategyFactory,
    DishkaWarehouseFactory,
)
from app.infra.shopping.position.reader import SqlAPositionReader


class ShoppingDomainServicesProvider(Provider):
    scope = Scope.APP

    category_services = provide(
        CategoryDomainService,
    )
    category_factories = provide_all(CategoryMediaKeyFactory)

    common_service = provide(PositionDomainService)

    services = provide_all(
        PositionFulfillmentDomainService,
        PositionWarehouseDomainService,
        scope=Scope.REQUEST,
    )
    position_factories = provide_all(
        PositionMediaKeyFactory,
    )
    item_factories = provide_all(FixedItemFactory, StockItemFactory)


class ShoppingHandlersProvider(Provider):
    scope = Scope.REQUEST

    category_commands = provide_all(
        ArchiveCategory,
        ArchiveAllCategories,
        ChangeCategoryDescriptionDefaultLang,
        ChangeCategoryNameDefaultLang,
        CreateCategory,
        DeleteCategory,
        DeleteAllCategories,
        DeleteCategoryMedia,
        RecoverCategory,
        RemoveCategoryDescription,
        RemoveCategoryName,
        SetCategoryDescription,
        SetCategoryName,
        SetCategoryMedia,
        TranslateCategoryNameToOthers,
        TranslateCategoryDescriptionToOthers,
        ArchivePositionItem,
    )

    category_queries = provide_all(
        GetCategory,
        GetCategoryShort,
        GetCategoryWithGoodsAmount,
        ListCategories,
        ListShortCategories,
    )

    position_commands = provide_all(
        AddPositionItems,
        AddPositionMedia,
        ArchiveAllPositionItems,
        ArchiveAllPositionsByCategory,
        ArchivePosition,
        ChangePositionDescriptionDefaultLang,
        ChangePositionNameDefaultLang,
        ChangePositionPriceBaseCurrency,
        ConvertPositionPriceToOthers,
        CreatePosition,
        DeleteAllPositionItems,
        DeleteAllPositionsByCategory,
        DeletePosition,
        DeletePositionItem,
        RecoverPosition,
        RecoverPositionItem,
        RemovePositionDescription,
        RemovePositionMedia,
        SetPositionDescription,
        SetPositionName,
        SetPositionPrice,
        TranslatePositionDescriptionToOthers,
        TranslatePositionNameToOthers,
    )

    position_queries = provide_all(
        GetPosition,
        GetPositionItem,
        GetPositionWithItemsAmount,
        ListPositionsByCategory,
        ListPositionItems,
        ListPositionsShortByCategory,
        ListPositionsWithItemsAmountByCategory,
    )


class ShoppingAdaptersProvider(Provider):
    scope = Scope.REQUEST

    position_repositories = provide_all(
        provide(SqlAFixedItemRepository, provides=FixedItemRepository),
        provide(SqlAStockItemRepository, provides=StockItemRepository),
        provide(SqlAPositionRepository, provides=PositionRepository),
    )
    position_repository = provide(SqlAPositionReader, provides=PositionReader)

    position_factories = provide_all(
        provide(PositionMediaKeyFactory, scope=Scope.APP),
        provide(DishkaWarehouseFactory, provides=WarehouseFactory),
        provide(
            DishkaFulfillmentStrategyFactory,
            provides=FulfillmentStrategyFactory,
        ),
    )

    position_strategies = provide_all(
        StockFulfillment, FixedFulfillment, FixedWarehouse, UnlimitedWarehouse
    )

    category_repository = provide(SqlACategoryRepository, provides=CategoryRepository)

    category_reader = provide(SqlACategoryReader, provides=CategoryReader)
