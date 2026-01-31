import sqlalchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.globals import exceptions as global_exceptions
from app.core.database import models


class UserRepository:

    @staticmethod
    async def select_user_by_id(user_id: int, session: AsyncSession):
        query = sqlalchemy.select(
            models.User.id,
            models.User.email,
            models.User.full_name,
            models.User.role,
        ).where(models.User.id == user_id)

        try:
            result = await session.execute(query)
            return result.mappings().first()
        except Exception as e:
            raise global_exceptions.DatabaseException(str(e))

    @staticmethod
    async def select_user_by_email(email: str, session: AsyncSession):
        query = sqlalchemy.select(
            models.User.id,
            models.User.email,
            models.User.full_name,
            models.User.hashed_password,
            models.User.role,
        ).where(models.User.email == email)

        try:
            result = await session.execute(query)
            return result.mappings().first()
        except Exception as e:
            raise global_exceptions.DatabaseException(str(e))

    @staticmethod
    async def insert_user(data: dict, session: AsyncSession):
        query = (
            sqlalchemy.insert(models.User)
            .values(**data)
            .returning(
                models.User.id,
                models.User.email,
                models.User.full_name,
                models.User.role,
            )
        )

        try:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()
        except Exception as e:
            raise global_exceptions.DatabaseException(str(e))

    @staticmethod
    async def update_user(user_id: int, data: dict, session: AsyncSession):
        query = (
            sqlalchemy.update(models.User)
            .where(models.User.id == user_id)
            .values(**data)
            .returning(
                models.User.id,
                models.User.email,
                models.User.full_name,
                models.User.role,
            )
        )

        try:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()
        except Exception as e:
            raise global_exceptions.DatabaseException(str(e))

    @staticmethod
    async def delete_user(user_id: int, session: AsyncSession):
        query = sqlalchemy.delete(models.User).where(models.User.id == user_id)

        try:
            await session.execute(query)
            await session.commit()
        except Exception as e:
            raise global_exceptions.DatabaseException(str(e))

    @staticmethod
    async def select_users(session: AsyncSession, limit: int, offset: int):

        account_subquery = (
            sqlalchemy.select(
                models.Account.user_id,
                sqlalchemy.func.coalesce(
                    sqlalchemy.func.jsonb_agg(
                        sqlalchemy.func.jsonb_build_object(
                            "id", models.Account.id, "balance", models.Account.balance
                        )
                    ),
                    sqlalchemy.func.cast("[]", JSONB),
                ).label("accounts"),
            ).group_by(models.Account.user_id)
        ).subquery()

        query = (
            sqlalchemy.select(
                models.User.id,
                models.User.email,
                models.User.full_name,
                models.User.role,
                sqlalchemy.func.coalesce(
                    account_subquery.c.accounts, sqlalchemy.func.cast("[]", JSONB)
                ).label("accounts"),
            )
            .outerjoin(account_subquery, account_subquery.c.user_id == models.User.id)
            .order_by(models.User.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        try:
            result = await session.execute(query)
            users = result.mappings().all()
            total_query = sqlalchemy.select(sqlalchemy.func.count()).select_from(
                models.User
            )
            total = (await session.execute(total_query)).scalar_one()
            return users, total
        except Exception as e:
            raise global_exceptions.DatabaseException(str(e))

    @staticmethod
    async def select_user_with_accounts(session: AsyncSession, user_id: int):

        account_subquery = (
            sqlalchemy.select(
                models.Account.user_id,
                sqlalchemy.func.coalesce(
                    sqlalchemy.func.jsonb_agg(
                        sqlalchemy.func.jsonb_build_object(
                            "id", models.Account.id, "balance", models.Account.balance
                        )
                    ),
                    sqlalchemy.func.cast("[]", JSONB),
                ).label("accounts"),
            )
            .where(models.Account.user_id == user_id)
            .group_by(models.Account.user_id)
        ).subquery()

        query = (
            sqlalchemy.select(
                models.User.id,
                models.User.email,
                models.User.full_name,
                models.User.role,
                sqlalchemy.func.coalesce(
                    account_subquery.c.accounts, sqlalchemy.func.cast("[]", JSONB)
                ).label("accounts"),
            )
            .outerjoin(account_subquery, account_subquery.c.user_id == models.User.id)
            .where(models.User.id == user_id)
        )

        try:
            result = await session.execute(query)
            user = result.mappings().first()
            return user
        except Exception as e:
            raise global_exceptions.DatabaseException(str(e))
