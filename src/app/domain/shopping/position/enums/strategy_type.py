from enum import StrEnum


class WarehouseType(StrEnum):
    FIXED = "FIXED"
    UNLIMITED = "UNLIMITED"


class FulfillmentType(StrEnum):
    FIXED = "FIXED"
    STOCK = "STOCK"
