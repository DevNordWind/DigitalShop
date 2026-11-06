from decimal import Decimal

import pytest

from app.domain.common.money import Currency, Money
from app.domain.wallet.exception import InsufficientFundsError
from tests.factory import WalletFactory


class TestWalletTopUp:
    @pytest.mark.parametrize(
        ("initial", "to_top_up", "expected"),
        [
            (
                pytest.param(
                    Money(amount=Decimal("100.00"), currency=Currency.USD),
                    Money(amount=Decimal("50.0"), currency=Currency.USD),
                    Money(amount=Decimal("150.0"), currency=Currency.USD),
                )
            ),
            (
                Money(amount=Decimal("1234.65"), currency=Currency.RUB),
                Money(amount=Decimal("234.56"), currency=Currency.RUB),
                Money(amount=Decimal("1469.21"), currency=Currency.RUB),
            ),
        ],
    )
    def test_top_up_increases_balance_by_given_amount(
        self, initial: Money, to_top_up: Money, expected: Money
    ) -> None:
        # Arrange
        wallet = WalletFactory.build(balance=initial)

        # Act
        wallet.top_up(to_top_up)

        # Assert
        assert wallet.balance == expected


class TestWalletWithdraw:
    @pytest.mark.parametrize(
        ("initial", "to_withdraw", "expected"),
        [
            (
                Money(amount=Decimal("100.00"), currency=Currency.USD),
                Money(amount=Decimal("50.0"), currency=Currency.USD),
                Money(amount=Decimal("50.0"), currency=Currency.USD),
            ),
            (
                Money(amount=Decimal("1234.65"), currency=Currency.RUB),
                Money(amount=Decimal("234.56"), currency=Currency.RUB),
                Money(amount=Decimal("1000.09"), currency=Currency.RUB),
            ),
        ],
    )
    def test_withdraw_decreases_balance_by_given_amount(
        self, initial: Money, to_withdraw: Money, expected: Money
    ) -> None:
        # Arrange
        wallet = WalletFactory.build(balance=initial)

        # Act
        wallet.withdraw(amount=to_withdraw)

        # Assert
        assert wallet.balance == expected

    @pytest.mark.parametrize(
        ("initial", "to_withdraw"),
        [
            (
                Money(amount=Decimal("150.00"), currency=Currency.RUB),
                Money(amount=Decimal("200.00"), currency=Currency.RUB),
            ),
            (
                Money(amount=Decimal("2135.43"), currency=Currency.KZT),
                Money(amount=Decimal("3000.00"), currency=Currency.KZT),
            ),
        ],
    )
    def test_withdraw_more_than_balance_is_rejected(
        self, initial: Money, to_withdraw: Money
    ) -> None:
        # Arrange
        wallet = WalletFactory.build(balance=initial)

        # Act & Assert
        with pytest.raises(InsufficientFundsError) as err:
            wallet.withdraw(amount=to_withdraw)

        assert wallet.balance == initial
        assert err.value.available == initial
