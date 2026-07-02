from app.domain.common.file_key import FileKeyError


class CategoryMediaKeyError(FileKeyError): ...


class CategoryMediaKeyMustBeMediaError(CategoryMediaKeyError): ...
