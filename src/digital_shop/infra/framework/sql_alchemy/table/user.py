from uuid import UUID

from domain.user.entity import User
from domain.user.enums import UserRole
from domain.user.value_object import UserId
from sqlalchemy import (
    UUID as SaUUID,  # noqa: N811
)
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import Composite, composite

from .base import mapper_registry, metadata

user_table: Table = Table(
    "User",
    metadata,
    Column("id", SaUUID, primary_key=True),
    Column("referrer_id", ForeignKey("User.id"), nullable=True),
    Column(
        "role",
        Enum(UserRole),
        nullable=False,
    ),
    Column("reg_at", DateTime(timezone=True), nullable=False),
)


def referrer_id_factory(value: UUID | None) -> UserId | None:
    if value is None:
        return None

    return UserId(value=value)


referrer_id_composite = composite(
    referrer_id_factory,
    user_table.c.referrer_id,
)
referrer_id_composite._generated_composite_accessor = lambda obj: (obj.value,)  # type: ignore[union-attr] # noqa: SLF001


def map_user() -> None:
    mapper_registry.map_imperatively(
        User,
        user_table,
        properties={
            "id": Composite(UserId, user_table.c.id),
            "_id": user_table.c.id,
            "referrer_id": referrer_id_composite,
            "_referrer_id": user_table.c.referrer_id,
        },
    )
