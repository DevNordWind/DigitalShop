from app.domain.common.coefficient import Coefficient
from app.domain.payment.enums import CommissionType, PaymentMethod
from app.domain.payment.exception import (
    CommissionCoefficientRequiredError,
)
from app.domain.payment.rule import (
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
            raise CommissionCoefficientRequiredError

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
