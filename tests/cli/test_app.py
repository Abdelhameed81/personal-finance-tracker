from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from unittest.mock import Mock
from urllib import request
from uuid import UUID

import callspec
import pytest
from _pytest.capture import CaptureFixture

from pytest import MonkeyPatch

from src.cli.app import ask_for_transaction_type, ask_for_transaction_amount, ask_for_transaction_description, \
    ask_for_transaction_category, run_app
from src.models.transaction import TransactionType, IncomeCategory, ExpenseCategory, Transaction
from src.repositories.json_transaction_repository import JsonTransactionRepository
from src.services.transaction_service import TransactionService


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
def test_ask_for_transaction_category(monkeypatch: MonkeyPatch, transaction_type: TransactionType,
                                      user_inputs: list[str],
                                      expected_return_category: IncomeCategory | ExpenseCategory) -> None:
    inputs = iter(user_inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert ask_for_transaction_category(transaction_type) == expected_return_category


@pytest.mark.parametrize("user_inputs", [
    pytest.param(["1", "Income", "55.05", "3", "test transaction", "5"],
                 id="Add transaction - happy path"),
])
def test_run_app_add_transaction_option(monkeypatch: MonkeyPatch, user_inputs: list[str]) -> None:
    transaction_service = Mock()
    inputs = iter(user_inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    run_app(transaction_service)
    transaction_service.add_transaction.assert_called_once()
    actual_transaction = transaction_service.add_transaction.call_args.args[0]
    assert actual_transaction.type == TransactionType.INCOME
    assert actual_transaction.amount == Decimal("55.05")
    assert actual_transaction.category == IncomeCategory.OTHER
    assert actual_transaction.description == "test transaction"
    assert isinstance(actual_transaction.date, datetime)
    assert isinstance(actual_transaction.uuid, UUID)


@pytest.mark.parametrize("transactions, expected_output", [
    pytest.param((), "There are no transactions",
                 id="View all transactions option with no transactions"),
    pytest.param(
        (Transaction(
            date=datetime.now(),
            type=TransactionType.INCOME,
            amount=Decimal("55.05"),
            category=IncomeCategory.OTHER,
            description="test transaction"),)
        , "test transaction",
        id="View all transactions option with transactions")
])
def test_run_app_view_all_transactions_option(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str],
                                              transactions: tuple[Transaction, ...], expected_output: str) -> None:
    transaction_service = Mock()
    transaction_service.transactions = transactions
    inputs = iter(["2", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    run_app(transaction_service)
    captured = capsys.readouterr()
    assert expected_output in captured.out


@pytest.mark.parametrize("transactions", [
    pytest.param((),
                 id="Remove transaction with no transactions"),
    pytest.param(
        (Transaction(
            date=datetime.now(),
            type=TransactionType.INCOME,
            amount=Decimal("55.05"),
            category=IncomeCategory.OTHER,
            description="test transaction"),),
        id="Remove transaction with transactions")
])
def test_run_app_remove_transaction_option(monkeypatch: MonkeyPatch,
                                           transactions: tuple[Transaction, ...]) -> None:
    transaction_service = Mock()
    transaction_service.transactions = transactions
    if transactions:
        uuid = transactions[0].uuid
        inputs = iter(["3", str(uuid), "5"])
    else:
        inputs = iter(["3", "5"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    run_app(transaction_service)

    if transactions:
        transaction_service.get_transaction_by_uuid.assert_called_once_with(str(transactions[0].uuid))
    else:
        transaction_service.get_transaction_by_uuid.assert_not_called()
