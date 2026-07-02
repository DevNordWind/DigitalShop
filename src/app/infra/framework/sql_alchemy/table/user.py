from sqlalchemy import Column, DateTime, Enum, ForeignKey, Table

from app.domain.user.entity import User
from app.domain.user.enums import UserRole

from .base import mapper_registry, metadata
from .custom_type import UserIdType

user_table: Table = Table(
    "User",
    metadata,
    Column("id", UserIdType, primary_key=True),
    Column("referrer_id", UserIdType, ForeignKey("User.id"), nullable=True),
    Column(
        "role",
        Enum(UserRole),
        nullable=False,
    ),
    Column("reg_at", DateTime(timezone=True), nullable=False),
)


def map_user() -> None:
    mapper_registry.map_imperatively(
        User,
        user_table,
    )
