from decimal import Decimal

import pytest

from app.domain.common.money import (
    Currency,
    CurrencyDifferenceError,
    NegativeMoneyAmountError,
)
from tests.factory import MoneyFactory


class TestMoneyInitialization:
    @pytest.mark.parametrize(
        "negative_amount",
        [
            Decimal("-0.00001"),
            Decimal("-1.00"),
            Decimal("-50.01"),
        ],
    )
    def test_raises_on_negative_amount(self, negative_amount: Decimal) -> None:
        # Act & Assert
        with pytest.raises(NegativeMoneyAmountError):
            MoneyFactory.build(amount=negative_amount)

    @pytest.mark.parametrize(
        ("raw_amount", "expected"),
        [
            pytest.param("0.125", "0.12", id="tie_rounds_down_to_even"),
            pytest.param("0.135", "0.14", id="tie_rounds_up_to_even"),
        ],
    )
    def test_uses_bank_rounding(self, raw_amount: str, expected: str) -> None:
        # Act
        money = MoneyFactory.build(amount=Decimal(raw_amount))

        # Assert
        assert money.amount == Decimal(expected)


class TestMoneyAdd:
    @pytest.mark.parametrize(
        ("orig", "other", "expected"),
        [
            (Decimal("100.00"), Decimal("50.00"), Decimal("150.00")),
            (Decimal("4312.34"), Decimal("3424.78"), Decimal("7737.12")),
        ],
    )
    def test_adds_amount(
        self, orig: Decimal, other: Decimal, expected: Decimal
    ) -> None:
        # Arrange
        orig_money = MoneyFactory.build(amount=orig)
        another_money = MoneyFactory.build(amount=other)

        # Act
        calculated = orig_money + another_money

        # Assert
        assert calculated.amount == expected

    def test_raises_on_different_currency(self) -> None:
        # Arrange
        orig_money = MoneyFactory.build(currency=Currency.RUB)
        another_money = MoneyFactory.build(currency=Currency.USD)

        # Act & Assert
        with pytest.raises(CurrencyDifferenceError):
            orig_money + another_money

    def test_rejects_non_money_operand(self) -> None:
        # Arrange
        orig_money = MoneyFactory.build()

        # Act & Assert
        with pytest.raises(TypeError):
            # pyrefly: ignore [unsupported-operation]
            orig_money + Decimal("1.00")


class TestMoneySub:
    @pytest.mark.parametrize(
        ("orig", "other", "expected"),
        [
            (Decimal("100.00"), Decimal("50.00"), Decimal("50.00")),
            (Decimal("4312.34"), Decimal("3424.78"), Decimal("887.56")),
        ],
    )
    def test_subtracts_amount(
        self, orig: Decimal, other: Decimal, expected: Decimal
    ) -> None:
        # Arrange
        orig_money = MoneyFactory.build(amount=orig)
        another_money = MoneyFactory.build(amount=other)

        # Act
        calculated = orig_money - another_money

        # Assert
        assert calculated.amount == expected

    def test_raises_on_different_currency(self) -> None:
        # Arrange
        orig_money = MoneyFactory.build(currency=Currency.RUB)
        another_money = MoneyFactory.build(currency=Currency.USD)

        # Act & Assert
        with pytest.raises(CurrencyDifferenceError):
            orig_money - another_money

    def test_rejects_non_money_operand(self) -> None:
        # Arrange
        orig_money = MoneyFactory.build()

        # Act & Assert
        with pytest.raises(TypeError):
            # pyrefly: ignore [unsupported-operation]
            orig_money + Decimal("1.00")

    @pytest.mark.parametrize(
        ("orig", "other"),
        [
            (Decimal("100.00"), Decimal("150.00")),
            (Decimal("4312.34"), Decimal("5424.78")),
        ],
    )
    def test_raises_when_result_would_be_negative(
        self, orig: Decimal, other: Decimal
    ) -> None:
        # Arrange
        orig_money = MoneyFactory.build(amount=orig)
        another_money = MoneyFactory.build(amount=other)

        # Act & Assert
        with pytest.raises(NegativeMoneyAmountError):
            orig_money - another_money


class TestMoneyMultiply:
    @pytest.mark.parametrize(
        ("orig", "factor", "expected"),
        [
            pytest.param(Decimal("10.00"), 3, Decimal("30.00"), id="int_factor"),
            pytest.param(
                Decimal("10.00"),
                Decimal("0.333"),
                Decimal("3.33"),
                id="decimal_factor_is_rounded",
            ),
        ],
    )
    def test_multiplies_amount(
        self, orig: Decimal, factor: Decimal | int, expected: Decimal
    ) -> None:
        # Arrange
        orig_amount = MoneyFactory.build(amount=orig)

        # Act
        calculated = orig_amount * factor

        # Assert
        assert calculated.amount == expected

    def test_rejects_another_factor_type(self) -> None:
        # Arrange
        orig_amount = MoneyFactory.build()

        # Act & Assert
        with pytest.raises(TypeError):
            # pyrefly: ignore [unsupported-operation]
            orig_amount * float("100.00")
