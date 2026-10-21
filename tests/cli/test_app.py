from decimal import Decimal

import pytest

from pytest import MonkeyPatch

from src.cli.app import ask_for_transaction_type, ask_for_transaction_amount, ask_for_transaction_description, \
    ask_for_transaction_category
from src.models.transaction import TransactionType, IncomeCategory, ExpenseCategory


@pytest.mark.parametrize(
    "user_inputs, expected_return_type",
    [
        pytest.param(["income"], TransactionType.INCOME, id="user entered income"),
        pytest.param(["expense"], TransactionType.EXPENSE, id="user entered expense"),
        pytest.param([" income "], TransactionType.INCOME, id="user entered income with spaces"),
        pytest.param(["blah blah", "expense"], TransactionType.EXPENSE, id="user entered blah blah then expense")
    ]
)
def test_ask_for_transaction_type(monkeypatch: MonkeyPatch, user_inputs: list[str],
                                  expected_return_type: TransactionType) -> None:
    inputs = iter(user_inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert ask_for_transaction_type() == expected_return_type


@pytest.mark.parametrize(
    "user_inputs, expected_return_amount",
    [
        pytest.param(["25"], Decimal("25"), id="Accept a whole amount, such as \"25\""),
        pytest.param(["25.5"], Decimal("25.5"), id="Accept one decimal place, such as \"25.5\""),
        pytest.param(["25.50"], Decimal("25.50"), id="Accept two decimal places, such as \"25.50\""),
        pytest.param(["0", "-1", "25.04"], Decimal("25.04"),
                     id="Reject zero and negative amounts, then ask again"),
        pytest.param(["text", "25.04"], Decimal("25.04"), id="Reject invalid text, then ask again"),
        pytest.param(["25.004", "25.04"], Decimal("25.04"),
                     id="Reject more than two decimal places, then ask again"),
    ]
)
def test_ask_for_amount(monkeypatch: MonkeyPatch, user_inputs: list[str],
                        expected_return_amount: Decimal) -> None:
    inputs = iter(user_inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert ask_for_transaction_amount() == expected_return_amount


@pytest.mark.parametrize(
    "user_inputs, expected_return_description",
    [
        pytest.param(["Weekly groceries"], "Weekly groceries", id="Normal description"),
        pytest.param(["  Monthly salary  "], "Monthly salary", id="Leading/trailing spaces"),
        pytest.param(["", "Groceries"], "Groceries", id="Empty input"),
        pytest.param(["   ", "Groceries"], "Groceries", id="Whitespace only"),
    ]
)
def test_ask_for_description(monkeypatch: MonkeyPatch, user_inputs: list[str],
                             expected_return_description: str) -> None:
    inputs = iter(user_inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert ask_for_transaction_description() == expected_return_description


@pytest.mark.parametrize(
    "transaction_type, user_inputs, expected_return_category",
    [
        pytest.param(TransactionType.INCOME, ["1"], IncomeCategory.SALARY, id="Income - user selects 1"),
        pytest.param(TransactionType.INCOME, ["3"], IncomeCategory.OTHER, id="Income - user selects 3"),
        pytest.param(TransactionType.EXPENSE, ["1"], ExpenseCategory.FOOD, id="Expense - user selects 1"),
        pytest.param(TransactionType.EXPENSE, ["5"], ExpenseCategory.CHILD_CARE, id="Expense - user selects 5"),
        pytest.param(TransactionType.EXPENSE, [" 2 "], ExpenseCategory.TRAVEL, id="Expense - user selects 2"),
        pytest.param(TransactionType.INCOME, ["5", "1"], IncomeCategory.SALARY,
                     id="Invalid number followed by valid choice"),
        pytest.param(TransactionType.INCOME, ["TEST", "1"], IncomeCategory.SALARY,
                     id="Non-numeric input followed by valid choice"),
    ]
)
def test_ask_transaction_category(monkeypatch: MonkeyPatch, transaction_type: TransactionType, user_inputs: list[str],
                                  expected_return_category: IncomeCategory | ExpenseCategory) -> None:
    inputs = iter(user_inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert ask_for_transaction_category(transaction_type) == expected_return_category
