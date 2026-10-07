from dataclasses import dataclass, field

from src.models import Transaction


@dataclass
class TransactionLedger:
    _transactions: list[Transaction] = field(default_factory=list)

    def add_transaction(self, transaction: Transaction) -> None:
        if not isinstance(transaction, Transaction):
            raise TypeError("Added transaction must be of type Transaction")
        self._transactions.append(transaction)

    @property
    def transactions(self) -> tuple[Transaction, ...]:
        return tuple(self._transactions)
