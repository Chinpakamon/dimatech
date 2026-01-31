"""Seed test users, accounts and payments"""

from alembic import op
from passlib.hash import bcrypt
import hashlib
from app.core.settings import settings

revision = "0002_seed_test_data"
down_revision = "e7955adadc4d"
branch_labels = None
depends_on = None


SECRET_KEY = settings.secret_key


def make_signature(account_id: int, amount: str, transaction_id: str, user_id: int) -> str:
    raw = f"{account_id}{amount}{transaction_id}{user_id}{SECRET_KEY}"
    return hashlib.sha256(raw.encode()).hexdigest()


def upgrade():
    user_password = bcrypt.hash("123456")
    admin_password = bcrypt.hash("admin123")

    op.execute(
        f"""
        INSERT INTO users (email, hashed_password, full_name, role, created_at)
        VALUES
        ('user@test.com', '{user_password}', 'Test User', 'USER', now()),
        ('admin@test.com', '{admin_password}', 'Admin User', 'ADMIN', now());
        """
    )

    op.execute("""
        INSERT INTO accounts (user_id, balance, created_at)
        VALUES
        (1, 0, now()),   -- user@test.com
        (1, 150.50, now()), 
        (2, 500.00, now()); -- admin@test.com
    """)

    payments = [
        ("TXN-1001", 1, 1, "100.00"),
        ("TXN-1002", 1, 1, "50.50"),
        ("TXN-2001", 1, 2, "200.00"),
        ("TXN-3001", 2, 3, "500.00"),
    ]

    values_sql = []

    for txn_id, user_id, acc_id, amount in payments:
        sign = make_signature(
            account_id=acc_id,
            amount=amount,
            transaction_id=txn_id,
            user_id=user_id,
        )
        values_sql.append(
            f"('{txn_id}', {user_id}, {acc_id}, {amount}, '{sign}', now())"
        )

    op.execute(
        f"""
        INSERT INTO payments (transaction_id, user_id, account_id, amount, signature, created_at)
        VALUES
        {",".join(values_sql)};
        """
    )


def downgrade():
    op.execute("DELETE FROM payments")
    op.execute("DELETE FROM accounts")
    op.execute("DELETE FROM users")
