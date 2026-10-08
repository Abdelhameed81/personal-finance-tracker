from datetime import datetime
from decimal import Decimal

import pytest

from src.transaction import Transaction, TransactionType, ExpenseCategory, IncomeCategory


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
