import re
from typing import Final

FILE_KEY_MAX_LENGTH: Final[int] = 512
FILE_KEY_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[a-z0-9/_-]+(\.[a-z0-9]{1,8})?$",
)
