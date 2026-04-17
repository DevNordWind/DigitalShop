from app.common.dto.money import MoneyMapper
from app.payment.dto.commission import CommissionSnapshotMapper
from app.payment.dto.payment.dto import PaymentDTO
from domain.payment.entity import Payment


class PaymentMapper:
    @classmethod
    def to_dto(cls, src: Payment) -> PaymentDTO:
        return PaymentDTO(
            id=src.id.value,
            creator_id=src.creator_id.value,
            purpose=src.purpose,
            original_amount=MoneyMapper.to_dto(src=src.original_amount),
            commission_snapshot=CommissionSnapshotMapper.to_dto(
                src=src.commission_snapshot,
            ),
            to_pay=MoneyMapper.to_dto(src=src.to_pay),
            status=src.status,
            method=src.method,
            external_id=src.external_id.value if src.external_id else None,
            created_at=src.created_at,
            updated_at=src.updated_at,
        )
