import hashlib
import json
import uuid

from app.core.settings import settings


def generate_signature(account_id: int, user_id: int, transaction_id: str, amount: float, secret_key: str) -> str:
    concatenated = f"{account_id}{amount}{transaction_id}{user_id}{secret_key}"
    return hashlib.sha256(concatenated.encode()).hexdigest()


def main():
    print("Генератор webhook payload ...")

    try:
        user_id = int(input("Введите user_id (по умолчанию 1): ") or 1)
        account_id = int(input("Введите account_id (по умолчанию 1): ") or 1)
        amount = float(input("Введите сумму пополнения (по умолчанию 100): ") or 100)
        transaction_id = input(
            "Введите transaction_id (оставьте пустым для генерации нового UUID): "
        ) or str(uuid.uuid4())
        secret_key = settings.secret_key

        signature = generate_signature(
            account_id, 
            user_id, 
            transaction_id, 
            amount, 
            secret_key
        )

        payload = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "account_id": account_id,
            "amount": amount,
            "signature": signature
        }

        print("\nСгенерированный payload ...")
        print(json.dumps(payload, indent=4))

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
