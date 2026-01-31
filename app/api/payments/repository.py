import decimal
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.globals import exceptions as global_exceptions
from app.core.database import models


class PaymentRepository:

    @staticmethod
    async def select_payments_by_user_id(user_id: int, session: AsyncSession):
        query = (
            sqlalchemy.select(
                models.Payment.id,
                models.Payment.transaction_id,
                models.Payment.account_id,
                models.Payment.amount,
                models.Payment.created_at,
                models.Payment.signature,
            )
            .where(models.Payment.user_id == user_id)
            .order_by(models.Payment.created_at.desc())
        )

        try:
            result = await session.execute(query)
            return result.mappings().all()
        except SQLAlchemyError as e:
            raise global_exceptions.DatabaseException(str(e))

    @staticmethod
    async def select_or_insert_account(user_id: int, account_id: int, session: AsyncSession):
        query = sqlalchemy.select(
            models.Account.id,
            models.Account.user_id,
            models.Account.balance
        ).where(
            models.Account.id == account_id,
            models.Account.user_id == user_id
        )

        try:
            result = await session.execute(query)
            account = result.mappings().first()

            if account:
                return account

            insert_query = (
                sqlalchemy.insert(models.Account)
                .values(
                    user_id=user_id,
                    balance=0
                )
                .returning(
                    models.Account.id,
                    models.Account.user_id,
                    models.Account.balance
                )
            )
            result = await session.execute(insert_query)
            await session.commit()
            return result.mappings().first()
        except SQLAlchemyError as e:
            raise global_exceptions.DatabaseException(str(e))

    @staticmethod
    async def payment_exists(transaction_id: int, session: AsyncSession) -> bool:
        query = sqlalchemy.select(sqlalchemy.exists().where(
            models.Payment.transaction_id == transaction_id)
        )
        result = await session.scalar(query)
        return bool(result)

    @staticmethod
    async def create_payment(payload: dict, session: AsyncSession):
        query = (
            sqlalchemy.insert(models.Payment)
            .values(**payload)
            .returning(
                models.Payment.transaction_id,
                models.Payment.account_id,
                models.Payment.user_id,
                models.Payment.amount,
                models.Payment.signature,
            )
        )
        try:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()
        except SQLAlchemyError as e:
            raise global_exceptions.DatabaseException(str(e))


    @staticmethod
    async def update_account_balance(account_id: int, amount: decimal.Decimal, session: AsyncSession):
        query = (
            sqlalchemy.update(models.Account)
            .where(models.Account.id == account_id)
            .values(balance=models.Account.balance + amount)
            .returning(
                models.Account.id,
                models.Account.user_id,
                models.Account.balance,
                models.Account.created_at,
                models.Account.updated_at,
            )
        )
        try:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()
        except SQLAlchemyError as e:
            raise global_exceptions.DatabaseException(str(e))
