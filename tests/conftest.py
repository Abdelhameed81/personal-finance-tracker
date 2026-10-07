from datetime import datetime
from decimal import Decimal

import pytest

from src.models import Transaction, TransactionType, ExpenseCategory


@pytest.fixture
def valid_transaction() -> Transaction:
    return Transaction(
        datetime(2026, 10, 5),
        TransactionType.EXPENSE,
        Decimal("42.50"),
        ExpenseCategory.FOOD,
        "Weekly shopping")
