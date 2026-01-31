import datetime
import decimal

import pydantic


class PaymentResponse(pydantic.BaseModel):
    id: int
    transaction_id: str
    account_id: int
    amount: decimal.Decimal
    created_at: datetime.datetime
    signature: str

    model_config = pydantic.ConfigDict(from_attributes=True)


class PaymentsListResponse(pydantic.BaseModel):
    payments: list[PaymentResponse] = []


class WebhookPayload(pydantic.BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: decimal.Decimal
    signature: str


class WebhookResponse(pydantic.BaseModel):
    user_id: int
    account_id: int
    account_balance: decimal.Decimal
