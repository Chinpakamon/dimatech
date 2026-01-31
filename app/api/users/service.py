from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users import exceptions, repository, schemas
from app.core.security.hashing import hash_password


class UserService:

    @staticmethod
    async def create_user(
        data: schemas.UserCreate, session: AsyncSession
    ) -> schemas.UserResponse:
        existing = await repository.UserRepository.select_user_by_email(
            email=data.email, session=session
        )
        if existing:
            raise exceptions.UserAlreadyExistsException()

        user_data = {
            "email": data.email,
            "hashed_password": hash_password(data.password),
            "full_name": data.full_name,
            "role": data.role,
        }

        try:
            user = await repository.UserRepository.insert_user(
                data=user_data, session=session
            )
        except Exception:
            raise exceptions.UserCreateFailedException()

        return schemas.UserResponse.model_validate(user)

    @staticmethod
    async def update_user(
        user_id: int, data: schemas.UserUpdate, session: AsyncSession
    ) -> schemas.UserResponse:
        user = await repository.UserRepository.select_user_by_id(
            user_id=user_id, session=session
        )
        if not user:
            raise exceptions.UserNotFoundException()

        update_data = {k: v for k, v in data.model_dump().items() if v is not None}

        updated = await repository.UserRepository.update_user(
            user_id=user_id, data=update_data, session=session
        )
        if not updated:
            raise exceptions.UserUpdateFailedException()

        return schemas.UserResponse(**updated)

    @staticmethod
    async def delete_user(
        user_id: int, session: AsyncSession
    ) -> schemas.DeleteUserResponse:
        user = await repository.UserRepository.select_user_by_id(
            user_id=user_id, session=session
        )
        if not user:
            raise exceptions.UserNotFoundException()

        try:
            await repository.UserRepository.delete_user(
                user_id=user.id, session=session
            )
            return schemas.DeleteUserResponse(success=True)
        except Exception:
            raise exceptions.UserDeleteFailedException()

    @staticmethod
    async def list_user(
        limit: int, offset: int, session: AsyncSession
    ) -> list[schemas.UserResponse]:
        users, total = await repository.UserRepository.select_users(
            session=session, limit=limit, offset=offset
        )

        data = [
            schemas.UserListItemResponse(
                id=u["id"],
                email=u["email"],
                full_name=u["full_name"],
                role=u["role"],
                accounts=[
                    schemas.AccountResponse(**acc) for acc in u.get("accounts", [])
                ],
            )
            for u in users
        ]

        return schemas.UserListResponse(
            data=data, total=total, limit=limit, offset=offset
        )

    @staticmethod
    async def get_user(user_id: int, session: AsyncSession) -> schemas.GetUserResponse:

        user = await repository.UserRepository.select_user_with_accounts(
            user_id=user_id, session=session
        )

        if not user:
            raise exceptions.UserNotFoundException()

        return schemas.GetUserResponse(**user)
