from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Enum,
    ForeignKey,
    String,
    Table,
)

from app.domain.common.localized import Language
from app.domain.common.money import Currency
from app.infra.authentication.telegram.model import TelegramContext

from .base import mapper_registry, metadata
from .custom_type import UserIdType, ZoneInfoType

telegram_context_table: Table = Table(
    "TelegramContext",
    metadata,
    Column("id", BigInteger, unique=True, index=True, nullable=False),
    Column("user_id", UserIdType, ForeignKey("User.id"), primary_key=True),
    Column("tg_username", String(length=64), nullable=True),
    Column("tg_first_name", String(length=64), nullable=False),
    Column("lang", Enum(Language), nullable=True),
    Column("currency", Enum(Currency), nullable=False),
    Column("timezone", ZoneInfoType, nullable=False),
    Column("is_active", Boolean, nullable=False),
)


def map_telegram_context() -> None:
    mapper_registry.map_imperatively(
        TelegramContext,
        telegram_context_table,
    )
