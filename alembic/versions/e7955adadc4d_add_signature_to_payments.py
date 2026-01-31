"""Add signature to payments

Revision ID: e7955adadc4d
Revises: dbf81ad03306
Create Date: 2026-01-31 08:38:32.768567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e7955adadc4d'
down_revision: Union[str, None] = 'dbf81ad03306'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('payments', sa.Column('signature', sa.String(length=255), nullable=False))
    op.create_index(op.f('ix_payments_signature'), 'payments', ['signature'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_payments_signature'), table_name='payments')
    op.drop_column('payments', 'signature')
