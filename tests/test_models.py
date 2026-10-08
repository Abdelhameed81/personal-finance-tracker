from datetime import datetime
from decimal import Decimal

import pytest

from src.transaction import Transaction, TransactionType, ExpenseCategory, IncomeCategory


def test_create_valid_expense_transaction(valid_expense_transaction: Transaction):
    assert valid_expense_transaction.date == datetime(2026, 10, 5)
    assert valid_expense_transaction.type == TransactionType.EXPENSE
    assert valid_expense_transaction.amount == Decimal("42.50")
    assert valid_expense_transaction.category == ExpenseCategory.FOOD
    assert valid_expense_transaction.description == "Weekly shopping"


def test_transaction_rejects_invalid_date():
    with pytest.raises(TypeError) as exc_info:
        Transaction(
            "06/10/2026",
            TransactionType.EXPENSE,
            Decimal("42.50"),
            ExpenseCategory.FOOD,
            "Weekly shopping")
    assert str(exc_info.value) == "Transaction date must be of type datetime"


def test_transaction_rejects_invalid_type():
    with pytest.raises(TypeError) as exc_info:
        Transaction(
            datetime(2026, 10, 5),
            None,
            Decimal("42.50"),
            ExpenseCategory.FOOD,
            "Weekly shopping")
    assert str(exc_info.value) == "Transaction type must be of type TransactionType"


@pytest.mark.parametrize("amount, expected_error, expected_error_message",
                         [
                             pytest.param(
                                 Decimal("0"),
                                 ValueError,
                                 "Transaction amount must be positive",
                                 id="Verify transaction raises ValueError exception when amount is zero"
                             ),
                             pytest.param(
                                 Decimal("-10"),
                                 ValueError,
                                 "Transaction amount must be positive",
                                 id="Verify transaction raises ValueError exception when amount is negative"
                             ),
                             pytest.param(
                                 10.5,
                                 TypeError,
                                 "Transaction amount must be of type Decimal",
                                 id="Verify transaction raises TypeError exception when amount is not of decimal type"
                             )
                         ]
                         )
def test_transaction_rejects_invalid_amount(amount: Decimal | float,
                                            expected_error: type[TypeError | ValueError],
                                            expected_error_message: str):
    with pytest.raises(expected_error) as exc_info:
        Transaction(
            datetime(2026, 10, 5),
            TransactionType.EXPENSE,
            amount,
            ExpenseCategory.FOOD,
            "Weekly shopping")
    assert str(exc_info.value) == expected_error_message


def test_transaction_rejects_invalid_category():
    with pytest.raises(TypeError) as exc_info:
        Transaction(
            datetime(2026, 10, 5),
            TransactionType.EXPENSE,
            Decimal("42.50"),
            None,
            "Weekly shopping")
    assert str(exc_info.value) == "Transaction category must be of type IncomeCategory or ExpenseCategory"


@pytest.mark.parametrize("transaction_type, transaction_category, expected_error_message",
                         [
                             pytest.param(
                                 TransactionType.INCOME,
                                 ExpenseCategory.FOOD,
                                 "Income transactions must be of type IncomeCategory",
                                 id="Verify a transaction of income type with expense category throws TypeError exception"
                             ),
                             pytest.param(
                                 TransactionType.EXPENSE,
                                 IncomeCategory.SALARY,
                                 "Expense transactions must be of type ExpenseCategory",
                                 id="Verify a transaction of expense type with income category throws TypeError exception"
                             )
                         ]
                         )
def test_transaction_rejects_mismatched_category(transaction_type: TransactionType,
                                                 transaction_category: IncomeCategory | ExpenseCategory,
                                                 expected_error_message: str):
    with pytest.raises(TypeError) as exc_info:
        Transaction(
            datetime(2026, 10, 5),
            transaction_type,
            Decimal("42.50"),
            transaction_category,
            "Weekly shopping")
    assert str(exc_info.value) == expected_error_message


def test_transaction_rejects_invalid_description_type():
    with pytest.raises(TypeError) as exc_info:
        Transaction(
            datetime(2026, 10, 5),
            TransactionType.EXPENSE,
            Decimal("42.50"),
            ExpenseCategory.FOOD,
            None)
    assert str(exc_info.value) == "Transaction description must be of type str"


@pytest.mark.parametrize("description", [
    pytest.param("", id="Empty description"),
    pytest.param(" ", id="White space description, verify strip"),
])
def test_transaction_rejects_empty_description(description: str):
    with pytest.raises(ValueError) as exc_info:
        Transaction(
            datetime(2026, 10, 5),
            TransactionType.EXPENSE,
            Decimal("42.50"),
            ExpenseCategory.FOOD,
            description)
    assert str(exc_info.value) == "Transaction description cannot be empty"
