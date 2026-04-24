from domain.common.money import Currency, Money
from domain.user.value_object import UserId
from domain.wallet.entity import Wallet
from domain.wallet.value_object import WalletId
from sqlalchemy import DECIMAL, UUID, Column, Enum, ForeignKey, Table
from sqlalchemy.orm import Composite

from .base import mapper_registry, metadata

wallet_table: Table = Table(
    "Wallet",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("user_id", ForeignKey("User.id"), nullable=False, index=True),
    Column("balance_currency", Enum(Currency), nullable=False),
    Column("balance_amount", DECIMAL(19, 4), nullable=False),
)


def map_wallet() -> None:
    mapper_registry.map_imperatively(
        Wallet,
        wallet_table,
        properties={
            "id": Composite(WalletId, wallet_table.c.id),
            "_id": wallet_table.c.id,
            "user_id": Composite(UserId, wallet_table.c.user_id),
            "_user_id": wallet_table.c.user_id,
            "balance": Composite(
                Money,
                wallet_table.c.balance_amount,
                wallet_table.c.balance_currency,
            ),
            "currency": wallet_table.c.balance_currency,
        },
    )
