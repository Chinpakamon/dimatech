import decimal

import sqlalchemy
from sqlalchemy import orm

from app.core import database
from app.core.database import mixins


class Payment(database.Base, mixins.PrimaryKeyMixin, mixins.TimestampMixin):
    __tablename__ = "payments"

    transaction_id: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    user_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    account_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
    )
    amount: orm.Mapped[decimal.Decimal] = orm.mapped_column(
        sqlalchemy.Numeric(12, 2),
        nullable=False,
    )
    signature: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(255), nullable=False, index=True
    )

    user = orm.relationship("User", back_populates="payments")
    account = orm.relationship("Account", back_populates="payments")
