import json
from datetime import datetime
from decimal import Decimal
from json import JSONDecodeError
from pathlib import Path
from uuid import UUID

from src.models.transaction import Transaction, TransactionType, IncomeCategory, ExpenseCategory


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

    def get_all_transactions(self) -> tuple[Transaction, ...]:
        if not self._json_file_path.is_file():
            return ()

        json_text = self._json_file_path.read_text(encoding="utf-8")
        json_data = json.loads(json_text)

        transactions = []
        for json_transaction in json_data:
            transactions.append(self._deserialize_transaction(json_transaction))
        return tuple(transactions)
