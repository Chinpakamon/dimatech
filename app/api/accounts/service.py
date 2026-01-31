from sqlalchemy.ext.asyncio import AsyncSession

from app.api.accounts import exceptions, repository, schemas
from app.api.globals import exceptions as global_exceptions


class AccountService:

    @staticmethod
    async def get_accounts_for_user(
        user_id: int, session: AsyncSession
    ) -> schemas.AccountsListResponse:
        try:
            accounts = await repository.AccountRepository.select_accounts_by_user_id(
                user_id=user_id, session=session
            )
        except global_exceptions.DatabaseException:
            raise exceptions.AccountsFetchFailedException()
        return schemas.AccountsListResponse(accounts=accounts)
