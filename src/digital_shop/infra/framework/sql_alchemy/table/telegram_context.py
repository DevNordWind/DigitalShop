from domain.common.localized import Language
from domain.common.money import Currency
from domain.user.value_object import UserId
from infra.authentication.telegram.model import TelegramContext
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Enum,
    ForeignKey,
    String,
    Table,
)
from sqlalchemy.orm import Composite

from .base import mapper_registry, metadata

telegram_context_table: Table = Table(
    "TelegramContext",
    metadata,
    Column("id", BigInteger, unique=True, index=True, nullable=False),
    Column("user_id", ForeignKey("User.id"), primary_key=True),
    Column("tg_username", String(length=64), nullable=True),
    Column("tg_first_name", String(length=64), nullable=False),
    Column("lang", Enum(Language), nullable=True),
    Column("currency", Enum(Currency), nullable=False),
    Column("is_active", Boolean, nullable=False),
)


def map_telegram_context() -> None:
    mapper_registry.map_imperatively(
        TelegramContext,
        telegram_context_table,
        properties={
            "user_id": Composite(UserId, telegram_context_table.c.user_id),
            "_user_id": telegram_context_table.c.user_id,
        },
    )
