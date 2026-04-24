from domain.common.file import FileKeyError


class CategoryMediaKeyError(FileKeyError): ...


class CategoryMediaKeyMustBeMediaError(CategoryMediaKeyError): ...
