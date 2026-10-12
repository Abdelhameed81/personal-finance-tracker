from decimal import Decimal
from json import JSONDecodeError
from pathlib import Path
from datetime import datetime
from uuid import UUID

import pytest

from src.models.transaction import Transaction, TransactionType, IncomeCategory
from src.repositories.json_transaction_repository import JsonTransactionRepository

"""
design rule is:
- Missing file → return ().
- Valid JSON containing [] → return ().
- Malformed JSON → raise json.JSONDecodeError.
- Zero-byte file → raise json.JSONDecodeError.
- Invalid transaction data → raise the relevant exception.
"""


@pytest.mark.parametrize("test_json_file", [
    pytest.param("", id="missing-file"),
    pytest.param("empty_transactions.json", id="empty-transactions")
])
def test_returns_empty_tuple_for_missing_or_empty_transactions_list(test_transaction_jsons_path: Path,
                                                                    test_json_file: str):
    json_path = test_transaction_jsons_path / test_json_file
    json_trans_repo = JsonTransactionRepository(json_path)
    transactions = json_trans_repo.get_all_transactions()
    assert isinstance(transactions, tuple)
    assert transactions == ()


@pytest.mark.parametrize("test_json_file", [
    pytest.param("malformed_json.json", id="malformed_json_file"),
    pytest.param("empty_file.json", id="empty_json_file")
])
def test_raises_json_decode_exception_for_malformed_or_empty_file(test_transaction_jsons_path: Path,
                                                                  test_json_file: str):
    json_path = test_transaction_jsons_path / test_json_file
    json_trans_repo = JsonTransactionRepository(json_path)
    with pytest.raises(JSONDecodeError):
        json_trans_repo.get_all_transactions()


def test_raises_exception_for_json_with_invalid_transaction_data(test_transaction_jsons_path: Path):
    json_path = test_transaction_jsons_path / "invalid_transaction_data.json"
    json_trans_repo = JsonTransactionRepository(json_path)
    with pytest.raises(TypeError):
        json_trans_repo.get_all_transactions()


def test_one_transaction(test_transaction_jsons_path: Path):
    json_path = test_transaction_jsons_path / "one_transaction.json"
    json_trans_repo = JsonTransactionRepository(json_path)
    transactions = json_trans_repo.get_all_transactions()
    assert isinstance(transactions, tuple)
    assert len(transactions) == 1
    assert isinstance(transactions[0], Transaction)
    assert transactions[0].date == datetime.fromisoformat("2024-10-09T14:32:00")
    assert transactions[0].type == TransactionType.INCOME
    assert transactions[0].amount == Decimal("1250.75")
    assert transactions[0].category == IncomeCategory.SALARY
    assert transactions[0].description == "October salary payment"
    assert transactions[0].uuid == UUID("8f14e45f-ea7b-4c1a-9b1e-3b2f4c9d9a12")


def test_multi_transactions(test_transaction_jsons_path: Path):
    json_path = test_transaction_jsons_path / "multi_transactions.json"
    json_trans_repo = JsonTransactionRepository(json_path)
    transactions = json_trans_repo.get_all_transactions()
    assert isinstance(transactions, tuple)
    assert all(isinstance(transaction, Transaction) for transaction in transactions)
    assert len(transactions) == 3
    assert transactions[0].description == "October salary payment"
    assert transactions[1].description == "Weekly groceries"
    assert transactions[2].description == "Utility bills"


def test_raises_key_error_exception_when_uuid_is_missing(test_transaction_jsons_path: Path):
    json_path = test_transaction_jsons_path / "missing_uuid.json"
    json_trans_repo = JsonTransactionRepository(json_path)
    with pytest.raises(KeyError):
        json_trans_repo.get_all_transactions()


def test_raises_value_error_exception_when_uuid_is_invalid(test_transaction_jsons_path: Path):
    json_path = test_transaction_jsons_path / "invalid_uuid.json"
    json_trans_repo = JsonTransactionRepository(json_path)
    with pytest.raises(ValueError):
        json_trans_repo.get_all_transactions()
