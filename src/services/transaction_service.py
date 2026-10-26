from uuid import UUID

from src.exceptions import TransactionNotFoundError
from src.models.transaction import Transaction
from src.models.transaction_ledger import TransactionLedger
from src.repositories.json_transaction_repository import JsonTransactionRepository


class TransactionService:
    def __init__(self, repo: JsonTransactionRepository) -> None:
        self._repo = repo
        self._ledger = TransactionLedger(self._repo.get_all_transactions())

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

    @property
    def transactions(self) -> tuple[Transaction, ...]:
        return self._ledger.transactions

    def get_transaction_by_uuid(self, transaction_uuid: UUID) -> Transaction | None:
        transactions = self._ledger.transactions
        for transaction in transactions:
            if transaction.uuid == transaction_uuid:
                return transaction
        return None
