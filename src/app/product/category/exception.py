from app.common.exception import ApplicationError


class CategoryApplicationError(ApplicationError): ...


class CategoryNotFound(CategoryApplicationError): ...
