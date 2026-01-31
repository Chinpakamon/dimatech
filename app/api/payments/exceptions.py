import fastapi


class PaymentsFetchFailedException(fastapi.HTTPException):
    def __init__(self):
        super().__init__(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch payments",
        )

class SignatureFailedException(fastapi.HTTPException):
    def __init__(self):
        super().__init__(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid signature",
        )

class TransactionAlreadyExistsException(fastapi.HTTPException):
    def __init__(self):
        super().__init__(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Transaction already exists",
        )