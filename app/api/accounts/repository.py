import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.globals import exceptions as global_exceptions
from app.core.database import models


class AccountRepository:

    @staticmethod
    async def select_accounts_by_user_id(user_id: int, session: AsyncSession):
        query = sqlalchemy.select(
            models.Account.id,
            models.Account.balance,
        ).where(models.Account.user_id == user_id)

        try:
            result = await session.execute(query)
            return result.mappings().all()
        except SQLAlchemyError as e:
            raise global_exceptions.DatabaseException(str(e))
