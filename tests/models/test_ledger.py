from decimal import Decimal

import pytest

from src.exceptions import TransactionNotFoundError
from src.models.ledger import TransactionLedger
from src.models.transaction import Transaction, TransactionType
from tests.conftest import valid_income_transaction


def test_ledger_transactions_is_unique_per_ledger_object():
    ledger_1 = TransactionLedger()
    ledger_2 = TransactionLedger()
    assert ledger_1._transactions is not ledger_2.transactions


def test_add_valid_transaction(valid_expense_transaction: Transaction):
    ledger = TransactionLedger()
    ledger.add_transaction(valid_expense_transaction)
    assert valid_expense_transaction in ledger.transactions


def test_add_invalid_transaction():
    ledger = TransactionLedger()
    with pytest.raises(TypeError) as exc_info:
        ledger.add_transaction("£42.50")
    assert str(exc_info.value) == "Added transaction must be of type Transaction"


def test_remove_valid_transaction(valid_expense_transaction: Transaction):
    ledger = TransactionLedger()
    ledger.add_transaction(valid_expense_transaction)
    ledger.remove_transaction(valid_expense_transaction)
    assert valid_expense_transaction not in ledger.transactions


def test_remove_invalid_transaction():
    ledger = TransactionLedger()
    with pytest.raises(TypeError) as exc_info:
        ledger.remove_transaction("£42.50")
    assert str(exc_info.value) == "Removed transaction must be of type Transaction"


def test_remove_transaction_not_in_ledger(valid_expense_transaction: Transaction):
    ledger = TransactionLedger()
    with pytest.raises(TransactionNotFoundError) as exc_info:
        ledger.remove_transaction(valid_expense_transaction)
    assert exc_info.value.transaction == valid_expense_transaction


def test_transactions_property_returns_tuple(valid_expense_transaction: Transaction):
    ledger = TransactionLedger()
    ledger.add_transaction(valid_expense_transaction)
    transactions = ledger.transactions
    assert isinstance(transactions, tuple)


def test_transactions_property_cannot_be_modified(valid_expense_transaction: Transaction):
    ledger = TransactionLedger()
    transactions = ledger.transactions
    with pytest.raises(AttributeError):
        transactions.append(valid_expense_transaction)


def test_empty_ledger_has_zero_balance():
    ledger = TransactionLedger()
    assert ledger.balance == Decimal("0")


def test_income_only_ledger_balance(valid_income_transaction: Transaction):
    ledger = TransactionLedger()
    ledger.add_transaction(valid_income_transaction)
    ledger.add_transaction(valid_income_transaction)
    assert ledger.balance == valid_income_transaction.amount * 2


def test_expense_only_ledger_balance(valid_expense_transaction: Transaction):
    ledger = TransactionLedger()
    ledger.add_transaction(valid_expense_transaction)
    ledger.add_transaction(valid_expense_transaction)
    assert ledger.balance == -valid_expense_transaction.amount * 2


def test_ledger_balance(valid_income_transaction: Transaction, valid_expense_transaction: Transaction):
    ledger = TransactionLedger()
    ledger.add_transaction(valid_income_transaction)
    ledger.add_transaction(valid_expense_transaction)
    assert ledger.balance == valid_income_transaction.amount - valid_expense_transaction.amount


def test_expenses_ledger_contains_only_expenses(valid_income_transaction: Transaction,
                                                valid_expense_transaction: Transaction):
    ledger = TransactionLedger()
    ledger.add_transaction(valid_income_transaction)
    ledger.add_transaction(valid_expense_transaction)
    ledger_expenses = ledger.expenses
    for transaction in ledger_expenses:
        assert transaction.type == TransactionType.EXPENSE


def test_incomes_ledger_returns_empty_tuple(valid_income_transaction: Transaction):
    ledger = TransactionLedger()
    ledger.add_transaction(valid_income_transaction)
    ledger.add_transaction(valid_income_transaction)
    assert not ledger.expenses


def test_expenses_property_cannot_be_modified(valid_expense_transaction: Transaction):
    ledger = TransactionLedger()
    ledger.add_transaction(valid_expense_transaction)
    ledger.add_transaction(valid_expense_transaction)
    ledger_expenses = ledger.expenses
    with pytest.raises(AttributeError):
        ledger_expenses.append(valid_expense_transaction)
