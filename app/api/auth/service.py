from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import exceptions, repository, schemas
from app.core import security


class AuthService:

    @staticmethod
    async def login(
        data: schemas.LoginRequest, session: AsyncSession
    ) -> schemas.LoginResponse:
        user = await repository.AuthRepository.select_user_by_email(
            email=data.email,
            session=session,
        )

        if not user or not security.verify_password(
            plain=data.password, hashed=user.hashed_password
        ):
            raise exceptions.InvalidCredentialsException()

        token = security.create_access_token(
            data={"user_id": str(user.id), "role": user.role.value}
        )

        return schemas.LoginResponse(access_token=token)
