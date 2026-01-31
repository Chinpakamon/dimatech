import enum

import sqlalchemy
from sqlalchemy import orm

from app.core import database
from app.core.database import mixins


class Role(enum.StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(database.Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    __tablename__ = "users"

    email: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(255), unique=True, index=True, nullable=False
    )
    hashed_password: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(255), nullable=False
    )
    full_name: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(255), nullable=False
    )
    role: orm.Mapped[Role] = orm.mapped_column(
        sqlalchemy.Enum(Role),
        default=Role.USER,
        nullable=False,
    )

    accounts = orm.relationship(
        "Account",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    payments = orm.relationship(
        "Payment",
        back_populates="user",
        cascade="all, delete-orphan",
    )
