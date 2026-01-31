from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users import schemas, service
from app.core.database.core import get_session
from app.core.middleware import dependencies

router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    "/me",
    response_model=schemas.UserMeResponse,
)
async def me(user=Depends(dependencies.get_current_user_dep)):
    return schemas.UserMeResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.value,
    )


@router.post(
    "/create",
    response_model=schemas.UserResponse,
    dependencies=[Depends(dependencies.require_admin)],
)
async def user_create(
    data: schemas.UserCreate, session: AsyncSession = Depends(get_session)
):
    return await service.UserService.create_user(data=data, session=session)


@router.post(
    "/update/{user_id}",
    response_model=schemas.UserResponse,
    dependencies=[Depends(dependencies.require_admin)],
)
async def user_update(
    user_id: int, data: schemas.UserUpdate, session: AsyncSession = Depends(get_session)
):
    return await service.UserService.update_user(
        user_id=user_id, data=data, session=session
    )


@router.post(
    "/delete/{user_id}",
    response_model=schemas.DeleteUserResponse,
    dependencies=[Depends(dependencies.require_admin)],
)
async def user_delete(user_id: int, session: AsyncSession = Depends(get_session)):
    return await service.UserService.delete_user(user_id=user_id, session=session)


@router.get(
    "/list",
    response_model=schemas.UserListResponse,
    dependencies=[Depends(dependencies.require_admin)],
)
async def user_list(
    limit: int = 10, offset: int = 0, session: AsyncSession = Depends(get_session)
):
    return await service.UserService.list_user(
        limit=limit, offset=offset, session=session
    )


@router.get(
    "/{user_id}",
    response_model=schemas.GetUserResponse,
    dependencies=[Depends(dependencies.require_admin)],
)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await service.UserService.get_user(user_id=user_id, session=session)
