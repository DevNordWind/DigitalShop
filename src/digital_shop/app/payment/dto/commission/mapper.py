from app.common.dto.coefficient import CoefficientMapper
from app.common.dto.money import MoneyMapper
from app.payment.dto.commission.dto import CommissionDTO, CommissionSnapshotDTO
from domain.payment.rule import (
    CustomerCommissionRule,
    PaymentCommissionRule,
    ShopCommissionRule,
)
from domain.payment.value_object import CommissionSnapshot


class CommissionMapper:
    @classmethod
    def to_dto(cls, src: PaymentCommissionRule) -> CommissionDTO:
        match src:
            case CustomerCommissionRule():
                return CommissionDTO(
                    type=src.type,
                    coefficient=CoefficientMapper.to_dto(src=src.coefficient),
                )
            case ShopCommissionRule():
                return CommissionDTO(type=src.type, coefficient=None)
            case _:
                raise ValueError(
                    f"Unknown PaymentCommissionRule type: {src.__class__.__name__}",  # noqa: E501
                )


class CommissionSnapshotMapper:
    @classmethod
    def to_value_object(cls, src: CommissionSnapshotDTO) -> CommissionSnapshot:
        return CommissionSnapshot(
            type=src.type,
            amount=MoneyMapper.to_value_object(src=src.amount),
            coefficient=CoefficientMapper.to_value_object(src=src.coefficient)
            if src.coefficient
            else None,
        )

    @classmethod
    def to_dto(cls, src: CommissionSnapshot) -> CommissionSnapshotDTO:
        return CommissionSnapshotDTO(
            type=src.type,
            amount=MoneyMapper.to_dto(
                src=src.amount,
            ),
            coefficient=CoefficientMapper.to_dto(src=src.coefficient)
            if src.coefficient
            else None,
        )
