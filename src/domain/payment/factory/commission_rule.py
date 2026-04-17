from domain.common.coefficient import Coefficient
from domain.payment.enums import CommissionType, PaymentMethod
from domain.payment.exception import (
    CommissionCoefficientRequired,
)
from domain.payment.rule import (
    CustomerCommissionRule,
    PaymentCommissionRule,
    ShopCommissionRule,
)


class PaymentCommissionRuleFactory:
    @classmethod
    def create(
        cls,
        method: PaymentMethod,
        tp: CommissionType,
        coefficient: Coefficient | None,
    ) -> PaymentCommissionRule:
        match tp:
            case CommissionType.CUSTOMER:
                return cls._create_customer(
                    method=method,
                    coefficient=coefficient,
                )
            case CommissionType.SHOP:
                return cls._create_shop(method=method)

    @classmethod
    def _create_customer(
        cls,
        method: PaymentMethod,
        coefficient: Coefficient | None,
    ) -> CustomerCommissionRule:
        if coefficient is None:
            raise CommissionCoefficientRequired

        return CustomerCommissionRule(
            payment_method=method,
            coefficient=coefficient,
        )

    @classmethod
    def _create_shop(
        cls,
        method: PaymentMethod,
    ) -> ShopCommissionRule:
        return ShopCommissionRule(
            payment_method=method,
        )
