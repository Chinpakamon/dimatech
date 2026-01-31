import pydantic

from app.api.users import consts


class UserMeResponse(pydantic.BaseModel):
    id: int
    email: pydantic.EmailStr
    full_name: str
    role: str


class UserCreate(pydantic.BaseModel):
    email: pydantic.EmailStr
    full_name: str
    password: str
    role: consts.Role = consts.Role.USER


class UserUpdate(pydantic.BaseModel):
    full_name: str | None = None
    role: consts.Role | None = None


class UserResponse(pydantic.BaseModel):
    id: int
    email: pydantic.EmailStr
    full_name: str
    role: consts.Role

    model_config = pydantic.ConfigDict(from_attributes=True)


class DeleteUserResponse(pydantic.BaseModel):
    success: bool


class AccountResponse(pydantic.BaseModel):
    id: int
    balance: float


class UserListItemResponse(pydantic.BaseModel):
    id: int
    email: pydantic.EmailStr
    full_name: str
    role: consts.Role
    accounts: list[AccountResponse] = []


class UserListResponse(pydantic.BaseModel):
    data: list[UserListItemResponse]
    total: int
    limit: int
    offset: int


class GetUserResponse(pydantic.BaseModel):
    id: int
    email: pydantic.EmailStr
    full_name: str
    role: consts.Role
    accounts: list[AccountResponse] = []
