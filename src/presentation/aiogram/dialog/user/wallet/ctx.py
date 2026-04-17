from dataclasses import dataclass
from typing import Final

CTX_KEY: Final[str] = "CTX"


@dataclass(slots=True)
class WalletCtx:
    show_all_balances: bool = False
