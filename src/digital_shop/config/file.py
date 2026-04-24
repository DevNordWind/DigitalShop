from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class FileStorageConfig:
    base_path: Path
