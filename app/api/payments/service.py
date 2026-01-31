from app.core import security
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.globals import exceptions as global_exceptions, repository as global_repository
from app.api.payments import exceptions, repository, schemas


class PaymentService:

    @staticmethod
    async def get_payments_for_user(
        user_id: int, session: AsyncSession
    ) -> schemas.PaymentsListResponse:
        try:
            payments = await repository.PaymentRepository.select_payments_by_user_id(
                user_id=user_id, session=session
            )
        except global_exceptions.DatabaseException:
            raise exceptions.PaymentsFetchFailedException()
        return schemas.PaymentsListResponse(payments=payments)

    @staticmethod
    async def process_webhook(
        payload: schemas.WebhookPayload, session: AsyncSession
    ) -> schemas.WebhookResponse:
        
        if not await security.verify_signature(payload=payload):
            raise exceptions.SignatureFailedException()
        
        user = await global_repository.UserRepository.select_user_by_id(
            user_id=payload.user_id, session=session
        )
        if not user:
            raise global_exceptions.UserNotFoundException()
        
        payment = await repository.PaymentRepository.payment_exists(
            transaction_id=payload.transaction_id, session=session)
        if payment:
            raise exceptions.TransactionAlreadyExistsException()
        
        account = await repository.PaymentRepository.select_or_insert_account(
            user_id=payload.user_id,
            account_id=payload.account_id,
            session=session
        )

        await repository.PaymentRepository.create_payment(
            payload=payload.model_dump(),session=session
        )

        account = await repository.PaymentRepository.update_account_balance(
            account_id=account.id, amount=payload.amount, session=session
        )

        return schemas.WebhookResponse(
            account_id=account.id, 
            account_balance=account.balance,
            user_id=payload.user_id
        )
