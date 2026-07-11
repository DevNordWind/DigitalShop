from abc import ABC, abstractmethod
from typing import Any, override

from app.app.common.dto.coefficient import CoefficientDTO
from app.domain.common.coefficient import (
    CoefficientTooBigError,
    CoefficientTooSmallError,
)
from app.domain.wallet.exception import InsufficientFundsError


class ErrorContextExtractor(ABC):
    @abstractmethod
    def extract(self, error: Exception) -> dict[str, Any]:
        raise NotImplementedError


class CoefficientErrorExtractor(ErrorContextExtractor):
    @override
    def extract(self, error: Exception) -> dict[str, Any]:
        if isinstance(error, CoefficientTooBigError):
            return {
                "max_percent": CoefficientDTO(value=error.max_coefficient).as_percent
            }
        if isinstance(error, CoefficientTooSmallError):
            return {
                "min_percent": CoefficientDTO(value=error.min_coefficient).as_percent
            }

        return {}


class InsufficientFundsErrorExtractor(ErrorContextExtractor):
    @override
    def extract(self, error: Exception) -> dict[str, Any]:
        if isinstance(error, InsufficientFundsError):
            return {
                "available_amount": error.available.amount,
                "currency": error.available.currency.value,
            }

        return {}
