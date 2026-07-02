from abc import abstractmethod
from datetime import datetime
from typing import Protocol


class Clock(Protocol):
    @abstractmethod
    def now(self) -> datetime: ...
