from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.payments import schemas, service
from app.core.database.core import get_session
from app.core.middleware import dependencies

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/me", response_model=schemas.PaymentsListResponse)
async def get_my_payments(
    current_user=Depends(dependencies.get_current_user_dep),
    session: AsyncSession = Depends(get_session),
):
    return await service.PaymentService.get_payments_for_user(
        user_id=current_user.id, session=session
    )


@router.post("/webhook", response_model=schemas.WebhookResponse)
async def payment_webhook(
    payload: schemas.WebhookPayload,
    session: AsyncSession = Depends(get_session),
):
    return await service.PaymentService.process_webhook(
        payload=payload, session=session
    )
