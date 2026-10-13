from src.exceptions import TransactionNotFoundError
from src.models.transaction import Transaction
from src.models.transaction_ledger import TransactionLedger
from src.repositories.json_transaction_repository import JsonTransactionRepository


class TransactionService:
    def __init__(self, ledger: TransactionLedger, repo: JsonTransactionRepository) -> None:
        if not isinstance(ledger, TransactionLedger):
            raise TypeError("TransactionLedger must be of type TransactionLedger")
        if not isinstance(repo, JsonTransactionRepository):
            raise TypeError("JsonTransactionRepository must be of type JsonTransactionRepository")
        self._ledger = ledger
        self._repo = repo

    def add_transaction(self, transaction: Transaction) -> None:
        if not isinstance(transaction, Transaction):
            raise TypeError("transaction must be of type Transaction")
        ledger_transactions = self._ledger.transactions
        updated_transactions = ledger_transactions + (transaction,)
        self._repo.save_all_transactions(updated_transactions)
        self._ledger.replace_transactions(updated_transactions)

    def remove_transaction(self, transaction: Transaction) -> None:
        if not isinstance(transaction, Transaction):
            raise TypeError("transaction must be of type Transaction")
        ledger_transactions = self._ledger.transactions
        if transaction not in ledger_transactions:
            raise TransactionNotFoundError(transaction)
        remove_first_occurrence = ledger_transactions.index(transaction)
        updated_transactions = ledger_transactions[:remove_first_occurrence] + ledger_transactions[
            remove_first_occurrence + 1:]
        self._repo.save_all_transactions(updated_transactions)
        self._ledger.replace_transactions(updated_transactions)
