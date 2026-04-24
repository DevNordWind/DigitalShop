from domain.product.position.enums.warehouse import WarehouseType
from domain.product.position.strategy import (
    FixedWarehouse,
    StockWarehouse,
    WarehouseStrategy,
)


class WarehouseFactory:
    @classmethod
    def create(cls, tp: WarehouseType) -> WarehouseStrategy:
        match tp:
            case WarehouseType.STOCK:
                return StockWarehouse()
            case WarehouseType.FIXED:
                return FixedWarehouse()
            case _:
                raise ValueError(f"Unknown warehouse type: {tp}")
