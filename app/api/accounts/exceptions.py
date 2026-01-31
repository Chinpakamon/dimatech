import fastapi


class AccountsFetchFailedException(fastapi.HTTPException):
    def __init__(self):
        super().__init__(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Failed to fetch accounts",
        )
