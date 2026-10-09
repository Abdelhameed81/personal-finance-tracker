from datetime import datetime
from decimal import Decimal

import pytest

from src.models.transaction_ledger import TransactionLedger
from src.models.transaction import Transaction, TransactionType, ExpenseCategory, IncomeCategory


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
    return TransactionLedger()


@pytest.fixture
def one_income_ledger(valid_income_transaction: Transaction) -> TransactionLedger:
    ledger = TransactionLedger()
    ledger.add_transaction(valid_income_transaction)
    return ledger


@pytest.fixture
def one_expense_ledger(valid_expense_transaction: Transaction) -> TransactionLedger:
    ledger = TransactionLedger()
    ledger.add_transaction(valid_expense_transaction)
    return ledger


@pytest.fixture
def multi_income_ledger(valid_income_transaction: Transaction) -> TransactionLedger:
    ledger = TransactionLedger()
    ledger.add_transaction(valid_income_transaction)
    ledger.add_transaction(valid_income_transaction)
    ledger.add_transaction(valid_income_transaction)
    return ledger


@pytest.fixture
def multi_expense_ledger(valid_expense_transaction: Transaction) -> TransactionLedger:
    ledger = TransactionLedger()
    ledger.add_transaction(valid_expense_transaction)
    ledger.add_transaction(valid_expense_transaction)
    ledger.add_transaction(valid_expense_transaction)
    return ledger


@pytest.fixture
def mixed_transaction_ledger(valid_income_transaction: Transaction,
                             valid_expense_transaction: Transaction) -> TransactionLedger:
    ledger = TransactionLedger()
    ledger.add_transaction(valid_income_transaction)
    ledger.add_transaction(valid_income_transaction)
    ledger.add_transaction(valid_expense_transaction)
    ledger.add_transaction(valid_expense_transaction)
    return ledger
