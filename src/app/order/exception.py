from app.common.exception import ApplicationError


class OrderApplicationError(ApplicationError): ...


class OrderNotFound(OrderApplicationError): ...
