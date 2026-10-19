from decimal import Decimal

import pytest

from pytest import MonkeyPatch

from src.cli.app import ask_for_transaction_type, ask_for_amount, ask_for_description
from src.models.transaction import TransactionType


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
    assert ask_for_amount() == expected_return_amount


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
    assert ask_for_description() == expected_return_description
