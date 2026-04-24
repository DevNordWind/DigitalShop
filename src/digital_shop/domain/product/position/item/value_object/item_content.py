from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from domain.product.position.item.enums import ItemContentType

T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class ItemContent(ABC):
    @property
    @abstractmethod
    def type(self) -> ItemContentType: ...

    @property
    @abstractmethod
    def value(self) -> object: ...


@dataclass(slots=True, frozen=True)
class TextItem(ItemContent):
    value: str

    @property
    def type(self) -> ItemContentType:
        return ItemContentType.TEXT


@dataclass(slots=True, frozen=True)
class ItemRaw(ABC):
    @property
    @abstractmethod
    def value(self) -> object: ...


@dataclass(slots=True, frozen=True)
class TextItemRaw(ItemRaw):
    value: str
