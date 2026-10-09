from src.exceptions import TransactionNotFoundError
from src.models.transaction import Transaction


class TransactionLedger:
    def __init__(self, transactions: tuple[Transaction, ...]):
        if not isinstance(transactions, tuple):
            raise TypeError("Transactions must be of type tuple")
        if not all(isinstance(transaction, Transaction) for transaction in transactions):
            raise TypeError("All transactions items must be of type Transaction")
        self._transactions = list(transactions)

    def add_transaction(self, transaction: Transaction) -> None:
        if not isinstance(transaction, Transaction):
            raise TypeError("Added transaction must be of type Transaction")
        self._transactions.append(transaction)

    def remove_transaction(self, transaction: Transaction) -> None:
        if not isinstance(transaction, Transaction):
            raise TypeError("Removed transaction must be of type Transaction")
        if transaction not in self._transactions:
            raise TransactionNotFoundError(transaction)
        self._transactions.remove(transaction)

    @property
    def transactions(self) -> tuple[Transaction, ...]:
        return tuple(self._transactions)
