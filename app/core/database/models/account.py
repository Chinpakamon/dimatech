import decimal

import sqlalchemy
from sqlalchemy import orm

from app.core import database
from app.core.database import mixins


class Account(database.Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    __tablename__ = "accounts"

    user_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    balance: orm.Mapped[decimal.Decimal] = orm.mapped_column(
        sqlalchemy.Numeric(12, 2),
        default=0,
        nullable=False,
    )

    user = orm.relationship("User", back_populates="accounts")
    payments = orm.relationship(
        "Payment",
        back_populates="account",
    )
