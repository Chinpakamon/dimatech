from contextlib import asynccontextmanager

import sqlalchemy
from fastapi import FastAPI, status

from app.api.accounts.router import router as accounts_router
from app.api.auth.router import router as auth_router
from app.api.payments.router import router as payments_router
from app.api.users.router import router as users_router
from app.core.database.core import engine
from app.core.middleware.auth_middleware import AuthMiddleware


async def check_db() -> None:
    async with engine.connect() as conn:
        await conn.execute(sqlalchemy.text("SELECT 1"))


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        await check_db()
        print("Database connected")
    except Exception as e:
        print("Database connection failed")
        raise e

    yield

    await engine.dispose()
    print("Database connections closed")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Dimatech API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(AuthMiddleware)

    app.include_router(accounts_router)
    app.include_router(payments_router)
    app.include_router(auth_router)
    app.include_router(users_router)

    @app.get(
        "/health",
        tags=["Healthcheck"],
        status_code=status.HTTP_200_OK,
    )
    async def healthcheck():
        try:
            await check_db()
            return {"status": "ok", "database": "ok"}
        except Exception:
            return {"status": "degraded", "database": "error"}

    return app


app = create_app()
