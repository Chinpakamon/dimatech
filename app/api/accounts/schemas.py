import decimal

import pydantic


class AccountResponse(pydantic.BaseModel):
    id: int
    balance: decimal.Decimal

    model_config = pydantic.ConfigDict(from_attributes=True)


class AccountsListResponse(pydantic.BaseModel):
    accounts: list[AccountResponse] = []
