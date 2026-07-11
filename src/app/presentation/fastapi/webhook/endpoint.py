import logging
from uuid import UUID

from aiocryptopay import AioCryptoPay
from aiocryptopay.const import InvoiceStatus
from aiocryptopay.models.update import Update
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from starlette.responses import Response

from app.app.payment.cmd import ConfirmPayment, ConfirmPaymentCmd
from app.domain.common.exception import DomainError
from fastapi import APIRouter, Depends, Header, HTTPException, Request

logger = logging.getLogger(__name__)

payments_router = APIRouter(prefix="/payments", tags=["Payments"])


@inject
async def verify_crypto_pay_signature(
    request: Request,
    crypto_pay: FromDishka[AioCryptoPay],
    crypto_pay_api_signature: str = Header(...),
) -> None:
    body = await request.body()
    if not crypto_pay.check_signature(
        body_text=body.decode(), crypto_pay_signature=crypto_pay_api_signature
    ):
        raise HTTPException(status_code=401)


@payments_router.post(
    "/crypto-pay", dependencies=[Depends(verify_crypto_pay_signature)]
)
@inject
async def handle_crypto_pay_update(
    crypto_pay_update: Update,
    handler: FromDishka[ConfirmPayment],
) -> Response:
    if crypto_pay_update.payload.status != InvoiceStatus.PAID:
        logger.debug(
            "Ignoring crypto pay update with status %s",
            crypto_pay_update.payload.status,
        )
        return Response(status_code=200)

    if crypto_pay_update.payload.payload is None:
        logger.debug("Ignoring crypto pay update without payload")
        return Response(status_code=200)

    try:
        await handler(ConfirmPaymentCmd(id=UUID(crypto_pay_update.payload.payload)))
    except DomainError as e:
        logger.info(e)
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)

    return Response(status_code=200)
