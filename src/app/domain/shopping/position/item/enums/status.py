from enum import StrEnum


class GenericItemStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    ARCHIVED = "ARCHIVED"


class StockItemStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    SOLD = "SOLD"
    ARCHIVED = "ARCHIVED"


class FixedItemStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    ARCHIVED = "ARCHIVED"
