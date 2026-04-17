from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class ResolvedByPath:
    value: Path


@dataclass(slots=True, frozen=True)
class ResolvedByUrl:
    value: str


ResolvedKey = ResolvedByUrl | ResolvedByPath
