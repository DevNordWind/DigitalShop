from typing import Any

from app.common.dto.coefficient import CoefficientMapper
from app.common.dto.money import MoneyDTO
from app.payment.dto.commission import CommissionSnapshotDTO
from app.payment.dto.payment import PaymentDTO
from domain.payment.value_object import PaymentPurpose


class PaymentReaderMapper:
    @classmethod
    def to_dto(cls, row: Any) -> PaymentDTO:
        return PaymentDTO(
            id=row.id,
            creator_id=row.creator_id,
            purpose=PaymentPurpose(
                reference_id=row.purpose_reference_id,
                type=row.purpose_type,
            ),
            original_amount=MoneyDTO(
                amount=row.original_amount_amount,
                currency=row.original_amount_currency,
            ),
            commission_snapshot=CommissionSnapshotDTO(
                type=row.commission_type,
                amount=MoneyDTO(
                    amount=row.commission_amount,
                    currency=row.original_amount_currency,
                ),
                coefficient=CoefficientMapper.to_dto(
                    src=row.commission_coefficient,
                )
                if row.commission_coefficient is not None
                else None,
            ),
            to_pay=MoneyDTO(
                amount=row.to_pay_amount,
                currency=row.original_amount_currency,
            ),
            status=row.status,
            method=row.method,
            external_id=row.external_id.value if row.external_id else None,
            created_at=row.created_id,
            updated_at=row.updated_at,
        )
