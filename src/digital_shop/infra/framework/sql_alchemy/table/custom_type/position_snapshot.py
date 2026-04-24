from decimal import Decimal
from typing import Any
from uuid import UUID

from domain.common.localized import Language, LocalizedText
from domain.common.money import Currency, Money
from domain.order.value_object import PositionSnapshot
from domain.product.position.value_object import PositionPrice
from frozendict import frozendict
from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB


class PositionSnapshotType(TypeDecorator[PositionSnapshot]):
    impl = JSONB
    cache_ok = True

    def process_bind_param(
        self,
        value: PositionSnapshot | None,
        dialect: Dialect,
    ) -> dict[str, Any] | None:
        if value is None:
            return None

        return {
            "category_id": str(value.category_id),
            "position_id": str(value.position_id),
            "position_name": {
                "default_lang": value.position_name.default_lang.value,
                "values": {
                    lang.value: text
                    for lang, text in value.position_name.values.items()
                },
            },
            "price": {
                "base_currency": value.price.base_currency.value,
                "prices": {
                    currency.value: str(money.amount)
                    for currency, money in value.price.prices.items()
                },
            },
        }

    def process_result_value(
        self,
        value: dict[str, Any] | None,
        dialect: Dialect,
    ) -> PositionSnapshot | None:
        if value is None:
            return None

        position_name = LocalizedText(
            default_lang=Language(value["position_name"]["default_lang"]),
            values=frozendict(
                {
                    Language(lang): text
                    for lang, text in value["position_name"]["values"].items()
                },
            ),
        )

        price = PositionPrice(
            base_currency=Currency(value["price"]["base_currency"]),
            prices=frozendict(
                {
                    Currency(currency): Money(
                        amount=Decimal(amount),
                        currency=Currency(currency),
                    )
                    for currency, amount in value["price"]["prices"].items()
                },
            ),
        )

        return PositionSnapshot(
            category_id=UUID(value["category_id"]),
            position_id=UUID(value["position_id"]),
            position_name=position_name,
            price=price,
        )
