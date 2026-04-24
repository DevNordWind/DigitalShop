import logging
from typing import Annotated
from uuid import UUID

from aiocryptopay import AioCryptoPay  # type: ignore[import-untyped]
from aiocryptopay.const import InvoiceStatus  # type: ignore[import-untyped]
from aiocryptopay.models.update import Update  # type: ignore[import-untyped]
from app.common.exception import ApplicationError
from app.payment.cmd import ConfirmPayment, ConfirmPaymentCmd
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from domain.common.exception import DomainError
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

payments_router = APIRouter(prefix="/payments")


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


@payments_router.post("/crypto_pay")
@inject
async def handle_crypto_pay_update(
    crypto_pay_update: Update,
    handler: FromDishka[ConfirmPayment],
    _: Annotated[None, Depends(verify_crypto_pay_signature)],
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
        await handler(
            ConfirmPaymentCmd(id=UUID(crypto_pay_update.payload.payload))
        )
    except (DomainError, ApplicationError) as e:
        logger.exception(e)
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)

    return Response(status_code=200)
