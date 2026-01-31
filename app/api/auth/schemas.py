import pydantic


class LoginRequest(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: str


class LoginResponse(pydantic.BaseModel):
    access_token: str
    token_type: str = "bearer"
