import hashlib
from app.api.payments import schemas
from app.core.settings import settings


async def verify_signature(payload: schemas.WebhookPayload) -> bool:
    concatenated = f"{payload.account_id}{payload.amount}{payload.transaction_id}{payload.user_id}{settings.secret_key}"
    calculated_signature = hashlib.sha256(concatenated.encode()).hexdigest()
    return calculated_signature == payload.signature
