from sqlalchemy import DECIMAL, Column, Enum, ForeignKey, Table
from sqlalchemy.orm import composite

from app.domain.common.money import Currency, Money
from app.domain.wallet.entity import Wallet

from .base import mapper_registry, metadata
from .custom_type import UserIdType, WalletIdType

wallet_table: Table = Table(
    "Wallet",
    metadata,
    Column("id", WalletIdType, primary_key=True),
    Column("user_id", UserIdType, ForeignKey("User.id"), nullable=False, index=True),
    Column("balance_currency", Enum(Currency), nullable=False),
    Column("balance_amount", DECIMAL(19, 4), nullable=False),
)


def map_wallet() -> None:
    mapper_registry.map_imperatively(
        Wallet,
        wallet_table,
        properties={
            "balance": composite(
                Money,
                wallet_table.c.balance_amount,
                wallet_table.c.balance_currency,
            ),
        },
    )
