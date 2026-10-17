from pathlib import Path

import pytest
from unittest.mock import Mock

from src.exceptions import TransactionNotFoundError
from src.models.transaction import Transaction
from src.models.transaction_ledger import TransactionLedger
from src.repositories.json_transaction_repository import JsonTransactionRepository
from src.services.transaction_service import TransactionService


def test_add_valid_transaction(valid_income_transaction: Transaction, valid_expense_transaction: Transaction,
                               tmp_path: Path) -> None:
    json_file = tmp_path / "test_add_valid_transaction.json"
    original_transactions = (valid_expense_transaction,)
    ledger = TransactionLedger(original_transactions)
    repo = JsonTransactionRepository(json_file)
    repo.save_all_transactions(original_transactions)
    service = TransactionService(ledger, repo)
    service.add_transaction(valid_income_transaction)
    expected_transactions = original_transactions + (valid_income_transaction,)
    assert ledger.transactions == expected_transactions
    assert repo.get_all_transactions() == expected_transactions


def test_add_invalid_transaction(valid_income_transaction: Transaction, valid_expense_transaction: Transaction,
                                 tmp_path: Path) -> None:
    json_file = tmp_path / "test_add_invalid_transaction.json"
    original_transactions = (valid_income_transaction, valid_expense_transaction)
    ledger = TransactionLedger(original_transactions)
    repo = JsonTransactionRepository(json_file)
    repo.save_all_transactions(original_transactions)
    service = TransactionService(ledger, repo)
    with pytest.raises(TypeError) as exc_info:
        service.add_transaction([])
    assert str(exc_info.value) == "transaction must be of type Transaction"
    assert ledger.transactions == original_transactions
    assert repo.get_all_transactions() == original_transactions


def test_add_transaction_repository_save_fails(valid_income_transaction: Transaction,
                                               valid_expense_transaction: Transaction) -> None:
    original_transactions = (valid_income_transaction,)
    ledger = TransactionLedger(original_transactions)
    mocked_repo = Mock(spec=JsonTransactionRepository)
    mocked_repo.save_all_transactions.side_effect = OSError("Simulated save failure")
    service = TransactionService(ledger, mocked_repo)
    with pytest.raises(OSError):
        service.add_transaction(valid_expense_transaction)
    assert ledger.transactions == original_transactions
    mocked_repo.save_all_transactions.assert_called_once_with((valid_income_transaction, valid_expense_transaction))


def test_remove_valid_transaction(valid_income_transaction: Transaction, valid_expense_transaction: Transaction,
                                  tmp_path: Path) -> None:
    json_file = tmp_path / "test_remove_valid_transaction.json"
    original_transactions = (valid_income_transaction, valid_expense_transaction, valid_income_transaction)
    ledger = TransactionLedger(original_transactions)
    repo = JsonTransactionRepository(json_file)
    repo.save_all_transactions(original_transactions)
    service = TransactionService(ledger, repo)
    service.remove_transaction(valid_income_transaction)
    assert ledger.transactions == (valid_expense_transaction, valid_income_transaction)
    assert repo.get_all_transactions() == (valid_expense_transaction, valid_income_transaction)


def test_remove_invalid_transaction(valid_income_transaction: Transaction, valid_expense_transaction: Transaction,
                                    tmp_path: Path) -> None:
    json_file = tmp_path / "test_remove_invalid_transaction.json"
    original_transactions = (valid_income_transaction, valid_expense_transaction)
    ledger = TransactionLedger(original_transactions)
    repo = JsonTransactionRepository(json_file)
    repo.save_all_transactions(original_transactions)
    service = TransactionService(ledger, repo)
    with pytest.raises(TypeError) as exc_info:
        service.remove_transaction([])
    assert str(exc_info.value) == "transaction must be of type Transaction"
    assert ledger.transactions == original_transactions
    assert repo.get_all_transactions() == original_transactions


def test_remove_unavailable_transaction(valid_income_transaction: Transaction, valid_expense_transaction: Transaction,
                                        tmp_path: Path) -> None:
    json_file = tmp_path / "test_remove_unavailable_transaction.json"
    original_transactions = (valid_expense_transaction,)
    ledger = TransactionLedger(original_transactions)
    repo = JsonTransactionRepository(json_file)
    repo.save_all_transactions(original_transactions)
    service = TransactionService(ledger, repo)
    with pytest.raises(TransactionNotFoundError) as exc_info:
        service.remove_transaction(valid_income_transaction)
    assert str(exc_info.value) == "This transaction does not exist in the ledger."
    assert ledger.transactions == original_transactions
    assert repo.get_all_transactions() == original_transactions


def test_remove_transaction_repository_save_fails(valid_income_transaction: Transaction,
                                                  valid_expense_transaction: Transaction) -> None:
    original_transactions = (valid_income_transaction, valid_expense_transaction)
    ledger = TransactionLedger(original_transactions)
    mocked_repo = Mock(spec=JsonTransactionRepository)
    mocked_repo.save_all_transactions.side_effect = OSError("Simulated save failure")
    service = TransactionService(ledger, mocked_repo)
    with pytest.raises(OSError):
        service.remove_transaction(valid_expense_transaction)
    assert ledger.transactions == original_transactions
    mocked_repo.save_all_transactions.assert_called_once_with((valid_income_transaction,))
