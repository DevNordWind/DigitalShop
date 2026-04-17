from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB

from domain.product.position.enums.warehouse import WarehouseType
from domain.product.position.service import WarehouseFactory
from domain.product.position.strategy import WarehouseStrategy


class WarehouseStrategyType(TypeDecorator[WarehouseStrategy]):
    impl = JSONB
    cache_ok = True

    def process_bind_param(
        self,
        value: WarehouseStrategy | None,
        dialect: Dialect,
    ) -> dict[str, str] | None:
        if value is None:
            return None

        return {"type": value.type.value}

    def process_result_value(
        self,
        value: dict[str, str] | None,
        dialect: Dialect,
    ) -> WarehouseStrategy | None:
        if value is None:
            return None

        tp = WarehouseType(value["type"])

        return WarehouseFactory.create(tp=tp)
