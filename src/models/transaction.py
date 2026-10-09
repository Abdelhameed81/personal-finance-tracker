from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass, field
from enum import Enum, auto
from uuid import UUID, uuid4


class TransactionType(Enum):
    INCOME = auto()
    EXPENSE = auto()


class IncomeCategory(Enum):
    SALARY = auto()
    BONUS = auto()
    OTHER = auto()


class ExpenseCategory(Enum):
    FOOD = auto()
    TRAVEL = auto()
    BILLS = auto()
    SHOPPING = auto()
    CHILD_CARE = auto()


@dataclass(frozen=True)
class Transaction:
    date: datetime
    type: TransactionType
    amount: Decimal
    category: IncomeCategory | ExpenseCategory
    description: str
    uuid: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if not isinstance(self.date, datetime):
            raise TypeError("Transaction date must be of type datetime")
        if not isinstance(self.type, TransactionType):
            raise TypeError("Transaction type must be of type TransactionType")
        if not isinstance(self.category, IncomeCategory | ExpenseCategory):
            raise TypeError("Transaction category must be of type IncomeCategory or ExpenseCategory")
        if self.type is TransactionType.INCOME and not isinstance(self.category, IncomeCategory):
            raise TypeError("Income transactions must be of type IncomeCategory")
        if self.type is TransactionType.EXPENSE and not isinstance(self.category, ExpenseCategory):
            raise TypeError("Expense transactions must be of type ExpenseCategory")
        if not isinstance(self.amount, Decimal):
            raise TypeError("Transaction amount must be of type Decimal")
        if self.amount <= 0:
            raise ValueError("Transaction amount must be positive")
        if not isinstance(self.description, str):
            raise TypeError("Transaction description must be of type str")
        if not self.description.strip():
            raise ValueError("Transaction description cannot be empty")
        if not isinstance(self.uuid, UUID):
            raise TypeError("Transaction uuid must be of type UUID")
