import pytest

from src.ledger import TransactionLedger
from src.models import Transaction


def test_ledger_transactions_is_unique_per_ledger_object():
    ledger_1 = TransactionLedger()
    ledger_2 = TransactionLedger()
    assert ledger_1._transactions is not ledger_2.transactions


def test_add_valid_transaction(valid_transaction: Transaction):
    ledger = TransactionLedger()
    ledger.add_transaction(valid_transaction)
    assert valid_transaction in ledger.transactions


def test_add_invalid_transaction():
    ledger = TransactionLedger()
    with pytest.raises(TypeError) as exc_info:
        ledger.add_transaction("£42.50")
    assert str(exc_info.value) == "Added transaction must be of type Transaction"


def test_transactions_property_returns_tuple(valid_transaction: Transaction):
    ledger = TransactionLedger()
    ledger.add_transaction(valid_transaction)
    transactions = ledger.transactions
    assert isinstance(transactions, tuple)


def test_transactions_property_cannot_be_modified(valid_transaction: Transaction):
    ledger = TransactionLedger()
    transactions = ledger.transactions
    with pytest.raises(AttributeError):
        transactions.append(valid_transaction)
