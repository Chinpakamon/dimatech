from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import schemas, service
from app.core.database.core import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.LoginResponse)
async def login(
    data: schemas.LoginRequest, session: AsyncSession = Depends(get_session)
):
    return await service.AuthService.login(data=data, session=session)
