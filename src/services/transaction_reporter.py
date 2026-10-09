from decimal import Decimal

from src.models.transaction import Transaction, TransactionType


class TransactionReporter:
    def __init__(self, transactions: tuple[Transaction, ...]) -> None:
        if not isinstance(transactions, tuple):
            raise TypeError("transactions must be a tuple")
        if not all(isinstance(transaction, Transaction) for transaction in transactions):
            raise TypeError("transactions tuple items must be of type Transaction")
        self._transactions = transactions

    def income_transactions(self) -> tuple[Transaction, ...]:
        return tuple(transaction for transaction in self._transactions if transaction.type == TransactionType.INCOME)

    def expense_transactions(self) -> tuple[Transaction, ...]:
        return tuple(transaction for transaction in self._transactions if transaction.type == TransactionType.EXPENSE)

    def total_income(self) -> Decimal:
        total_incomes = Decimal(0)
        for transaction in self.income_transactions():
            total_incomes += transaction.amount
        return total_incomes

    def total_expenses(self) -> Decimal:
        total_expenses = Decimal(0)
        for transaction in self.expense_transactions():
            total_expenses += transaction.amount
        return total_expenses

    @property
    def balance(self) -> Decimal:
        return self.total_income() - self.total_expenses()
