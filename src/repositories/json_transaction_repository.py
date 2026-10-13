import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from uuid import UUID

from src.models.transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory

"""
design rule is:
- Missing file → return ().
- Valid JSON containing [] → return ().
- Malformed JSON → raise json.JSONDecodeError.
- Zero-byte file → raise json.JSONDecodeError.
- Invalid transaction data → raise the relevant exception.
"""


class JsonTransactionRepository:
    def __init__(self, json_file_path: Path) -> None:
        self._json_file_path = json_file_path

    @staticmethod
    def _deserialize_transaction(json_transaction: dict[str, str]) -> Transaction:
        transaction_type = TransactionType[json_transaction["type"]]
        category: IncomeCategory | ExpenseCategory
        try:
            category = IncomeCategory[json_transaction["category"]]
        except KeyError:
            category = ExpenseCategory[json_transaction["category"]]

        return Transaction(
            date=datetime.fromisoformat(json_transaction["date"]),
            type=transaction_type,
            amount=Decimal(json_transaction["amount"]),
            category=category,
            description=json_transaction["description"],
            uuid=UUID(json_transaction["uuid"]),
        )

    @staticmethod
    def _serialize_transaction(transaction: Transaction) -> dict[str, str]:
        return {
            "date": transaction.date.isoformat(),
            "type": transaction.type.name,
            "amount": str(transaction.amount),
            "category": transaction.category.name,
            "description": transaction.description,
            "uuid": str(transaction.uuid),
        }

    def get_all_transactions(self) -> tuple[Transaction, ...]:
        if not self._json_file_path.is_file():
            return ()

        json_text = self._json_file_path.read_text(encoding="utf-8")
        json_transactions_data = json.loads(json_text)

        transactions = [self._deserialize_transaction(transaction) for transaction in json_transactions_data]
        return tuple(transactions)

    def save_all_transactions(self, transactions: tuple[Transaction, ...]) -> None:
        if not isinstance(transactions, tuple):
            raise TypeError("transactions must be of type tuple")
        if not all(isinstance(transaction, Transaction) for transaction in transactions):
            raise TypeError("All transactions items must be of type Transaction")
        transactions_list = [self._serialize_transaction(transaction) for transaction in transactions]
        transactions_text = json.dumps(transactions_list, indent=2)
        self._json_file_path.write_text(transactions_text, encoding="utf-8")
