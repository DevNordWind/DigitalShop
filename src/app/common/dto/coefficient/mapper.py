from app.common.dto.coefficient.dto import CoefficientDTO
from domain.common.coefficient import Coefficient


class CoefficientMapper:
    @classmethod
    def to_value_object(cls, src: CoefficientDTO) -> Coefficient:
        return Coefficient(value=src.value)

    @classmethod
    def to_dto(cls, src: Coefficient) -> CoefficientDTO:
        return CoefficientDTO(value=src.value)
