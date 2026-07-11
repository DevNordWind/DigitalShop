from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ItemContentDTO:
    value: str
