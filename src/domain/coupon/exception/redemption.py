from domain.common.exception import DomainError


class CouponRedemptionError(DomainError): ...


class CouponRedemptionCancellationForbidden(CouponRedemptionError): ...


class CouponRedemptionConfirmationForbidden(CouponRedemptionError): ...
