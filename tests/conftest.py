from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Generator
from uuid import UUID

import pytest

from src.models.transaction_ledger import TransactionLedger
from src.models.transaction import Transaction, TransactionType, ExpenseCategory, IncomeCategory
from src.repositories.json_transaction_repository import JsonTransactionRepository

known_id = UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def transaction_as_dict() -> dict[str, str]:
    return {
        "date": "2024-10-09T14:32:00",
        "type": "INCOME",
        "amount": "1250.75",
        "category": "SALARY",
        "description": "October salary payment",
        "uuid": "8f14e45f-ea7b-4c1a-9b1e-3b2f4c9d9a12"
    }


@pytest.fixture
def valid_expense_transaction() -> Transaction:
    return Transaction(
        datetime(2026, 10, 5),
        TransactionType.EXPENSE,
        Decimal("42.50"),
        ExpenseCategory.FOOD,
        "Weekly shopping")


@pytest.fixture
def valid_income_transaction() -> Transaction:
    return Transaction(
        datetime(2026, 10, 5),
        TransactionType.INCOME,
        Decimal("42.50"),
        IncomeCategory.SALARY,
        "Monthly salary")


# @pytest.fixture
# def ledger(transactions: tuple[Transaction, ...]) -> TransactionLedger:
#     ledger = TransactionLedger()
#     for transaction in transactions:
#         ledger.add_transaction(transaction)
#     return ledger


@pytest.fixture
def empty_ledger() -> TransactionLedger:
    return TransactionLedger(())


@pytest.fixture
def one_income_ledger(valid_income_transaction: Transaction) -> TransactionLedger:
    ledger = TransactionLedger((valid_income_transaction,))
    return ledger


@pytest.fixture
def one_expense_ledger(valid_expense_transaction: Transaction) -> TransactionLedger:
    ledger = TransactionLedger((valid_expense_transaction,))
    return ledger


@pytest.fixture
def multi_income_ledger(valid_income_transaction: Transaction) -> TransactionLedger:
    ledger = TransactionLedger((valid_income_transaction,) * 3)
    return ledger


@pytest.fixture
def multi_expense_ledger(valid_expense_transaction: Transaction) -> TransactionLedger:
    ledger = TransactionLedger((valid_expense_transaction,) * 3)
    return ledger


@pytest.fixture
def mixed_transaction_ledger(valid_income_transaction: Transaction,
                             valid_expense_transaction: Transaction) -> TransactionLedger:
    transactions = (valid_income_transaction,) * 2 + (valid_expense_transaction,) * 2
    ledger = TransactionLedger(transactions)
    return ledger


@pytest.fixture
def test_transaction_jsons_path() -> Path:
    project_root = Path(__file__).resolve().parent
    json_path = project_root / "data"
    return json_path
