from app.common.exception import ApplicationError


class CouponApplicationError(ApplicationError): ...


class CouponNotFound(CouponApplicationError): ...
