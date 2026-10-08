from dataclasses import dataclass, field
from decimal import Decimal

from src.exceptions import TransactionNotFoundError
from src.models.transaction import Transaction, TransactionType


@dataclass
class TransactionLedger:
    _transactions: list[Transaction] = field(default_factory=list)

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

    @property
    def expenses(self) -> tuple[Transaction, ...]:
        return tuple(transaction for transaction in self._transactions if transaction.type is TransactionType.EXPENSE)

    @property
    def balance(self) -> Decimal:
        balance = Decimal("0.00")
        for transaction in self.transactions:
            if transaction.type is TransactionType.INCOME:
                balance += transaction.amount
            elif transaction.type is TransactionType.EXPENSE:
                balance -= transaction.amount
        return balance
