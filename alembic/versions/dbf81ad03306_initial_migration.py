"""Initial migration

Revision ID: dbf81ad03306
Revises: 
Create Date: 2026-01-28 17:08:19.509557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'dbf81ad03306'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('role', sa.Enum('USER', 'ADMIN', name='role'), nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=True, start=1), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('accounts',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('balance', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=True, start=1), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_accounts_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_accounts'))
    )
    op.create_index(op.f('ix_accounts_user_id'), 'accounts', ['user_id'], unique=False)
    op.create_table('payments',
    sa.Column('transaction_id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('account_id', sa.BigInteger(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=True, start=1), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], name=op.f('fk_payments_account_id_accounts'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_payments_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_payments'))
    )
    op.create_index(op.f('ix_payments_transaction_id'), 'payments', ['transaction_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_payments_transaction_id'), table_name='payments')
    op.drop_table('payments')
    op.drop_index(op.f('ix_accounts_user_id'), table_name='accounts')
    op.drop_table('accounts')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

    # Подойдет для такого маленького проекта, не production-safe
    op.execute("DROP TYPE IF EXISTS role")
