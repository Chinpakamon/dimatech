from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.accounts import schemas, service
from app.core.database.core import get_session
from app.core.middleware.dependencies import get_current_user_dep

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/me", response_model=schemas.AccountsListResponse)
async def get_my_accounts(
    current_user=Depends(get_current_user_dep),
    session: AsyncSession = Depends(get_session),
):
    return await service.AccountService.get_accounts_for_user(
        user_id=current_user.id, session=session
    )
