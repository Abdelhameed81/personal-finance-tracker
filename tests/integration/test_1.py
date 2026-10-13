from pathlib import Path

from src.models.transaction import Transaction
from src.models.transaction_ledger import TransactionLedger
from src.repositories.json_transaction_repository import JsonTransactionRepository


def test_ledger_initialised_with_transactions_loaded_from_repository(tmp_path: Path,
                                                                     valid_income_transaction: Transaction,
                                                                     valid_expense_transaction: Transaction) -> None:
    json_file = tmp_path / "integration_test_file.json"
    json_trans_repo = JsonTransactionRepository(json_file)
    original_transactions = (valid_income_transaction, valid_expense_transaction)
    json_trans_repo.save_all_transactions(original_transactions)
    loaded_transactions = json_trans_repo.get_all_transactions()
    ledger = TransactionLedger(loaded_transactions)
    assert ledger.transactions == loaded_transactions


def test_ledger_syncs_with_repository(tmp_path: Path,
                                      valid_income_transaction: Transaction,
                                      valid_expense_transaction: Transaction) -> None:
    json_file = tmp_path / "integration_test_file.json"
    json_trans_repo = JsonTransactionRepository(json_file)
    original_transactions = (valid_income_transaction,)
    json_trans_repo.save_all_transactions(original_transactions)
    ledger = TransactionLedger(json_trans_repo.get_all_transactions())
    ledger.add_transaction(valid_expense_transaction)
    updated_transactions = ledger.transactions
    json_trans_repo.save_all_transactions(updated_transactions)
    loaded_transactions = json_trans_repo.get_all_transactions()
    expected_transactions = (
        valid_income_transaction,
        valid_expense_transaction,
    )
    assert loaded_transactions == expected_transactions
