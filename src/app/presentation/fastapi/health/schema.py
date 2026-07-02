from dataclasses import dataclass
from typing import Final, Literal


@dataclass(slots=True, frozen=True)
class OkResponse:
    status: Literal["ok"]


OK_RESPONSE: Final[OkResponse] = OkResponse(status="ok")
