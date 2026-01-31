from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import models


class AuthRepository:

    @staticmethod
    async def select_user_by_email(
        email: str, session: AsyncSession
    ) -> models.User | None:
        query = select(models.User).where(models.User.email == email)
        return await session.scalar(query)
