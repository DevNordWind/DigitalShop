from decimal import Decimal
from typing import Any

from domain.common.coefficient import Coefficient
from domain.common.money import Currency, Money
from domain.payment.entity import Payment
from domain.payment.enums import (
    CommissionType,
    PaymentMethod,
    PaymentPurposeType,
    PaymentStatus,
)
from domain.payment.rule import (
    CustomerCommissionRule,
    PaymentCommissionRule,
    ShopCommissionRule,
)
from domain.payment.value_object import (
    CommissionSnapshot,
    PaymentId,
    PaymentPurpose,
)
from domain.user.value_object import UserId
from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    Table,
    event,
)
from sqlalchemy.orm import Composite

from .base import mapper_registry, metadata
from .custom_type import PaymentExternalIdType

payment_table: Table = Table(
    "Payment",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("creator_id", ForeignKey("User.id"), nullable=False),
    Column("purpose_reference_id", UUID, nullable=False),
    Column("purpose_type", Enum(PaymentPurposeType), nullable=False),
    Column("original_amount_amount", Numeric(19, 4), nullable=False),
    Column("original_amount_currency", Enum(Currency), nullable=False),
    Column("to_pay_amount", Numeric(19, 4), nullable=False),
    Column("commission_type", Enum(CommissionType), nullable=False),
    Column(
        "commission_coefficient",
        Numeric(precision=4, scale=3),
        nullable=True,
    ),
    Column("commission_amount", Numeric(19, 4), nullable=False),
    Column("method", Enum(PaymentMethod), nullable=False),
    Column("status", Enum(PaymentStatus), nullable=False),
    Column("external_id", PaymentExternalIdType, nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
)

payment_commission_rule_table: Table = Table(
    "PaymentCommissionRule",
    metadata,
    Column("payment_method", Enum(PaymentMethod), primary_key=True),
    Column("type", Enum(CommissionType), nullable=False),
    Column("coefficient", Numeric(precision=4, scale=3), nullable=True),
)


def compose_commission(
    tp: CommissionType,
    amount: Decimal,
    currency: Currency,
    coefficient: Decimal | None,
) -> CommissionSnapshot:
    return CommissionSnapshot(
        type=tp,
        amount=Money(amount, currency),
        coefficient=Coefficient(value=coefficient)
        if coefficient is not None
        else None,
    )


composite_commission = Composite(
    compose_commission,
    payment_table.c.commission_type,
    payment_table.c.commission_amount,
    payment_table.c.original_amount_currency,
    payment_table.c.commission_coefficient,
)
composite_commission._generated_composite_accessor = lambda obj: (  # noqa: SLF001
    obj.type,
    obj.amount.amount,
    obj.amount.currency,
    obj.coefficient.value if obj.coefficient is not None else None,
)


def calculate_to_pay(_: Any, __: Any, target: Payment) -> None:
    target.__dict__["_to_pay_amount"] = target.to_pay.amount


def calculate_type(_: Any, __: Any, target: PaymentCommissionRule) -> None:
    target.__dict__["_type"] = target.type


def map_payment() -> None:
    mapper_registry.map_imperatively(
        Payment,
        payment_table,
        properties={
            "id": Composite(PaymentId, payment_table.c.id),
            "_id": payment_table.c.id,
            "creator_id": Composite(UserId, payment_table.c.creator_id),
            "_creator_id": payment_table.c.creator_id,
            "purpose": Composite(
                PaymentPurpose,
                payment_table.c.purpose_reference_id,
                payment_table.c.purpose_type,
            ),
            "original_amount": Composite(
                Money,
                payment_table.c.original_amount_amount,
                payment_table.c.original_amount_currency,
            ),
            "commission_snapshot": composite_commission,
            "_to_pay_amount": payment_table.c.to_pay_amount,
        },
    )
    event.listen(Payment, "before_insert", calculate_to_pay)
    event.listen(Payment, "before_update", calculate_to_pay)


def map_payment_commission_rule() -> None:
    mapper_registry.map_imperatively(
        PaymentCommissionRule,  # type: ignore[type-abstract]
        payment_commission_rule_table,
        polymorphic_on=payment_commission_rule_table.c.type,
        properties={
            "_type": payment_commission_rule_table.c.type,
        },
    )
    mapper_registry.map_imperatively(
        CustomerCommissionRule,
        payment_commission_rule_table,
        inherits=PaymentCommissionRule,
        polymorphic_identity=CommissionType.CUSTOMER,
        properties={
            "coefficient": Composite(
                Coefficient,
                payment_commission_rule_table.c.coefficient,
            ),
            "_coefficient": payment_commission_rule_table.c.coefficient,
        },
    )
    mapper_registry.map_imperatively(
        ShopCommissionRule,
        payment_commission_rule_table,
        inherits=PaymentCommissionRule,
        polymorphic_identity=CommissionType.SHOP,
    )
    event.listen(PaymentCommissionRule, "before_insert", calculate_type)
    event.listen(PaymentCommissionRule, "before_update", calculate_type)
