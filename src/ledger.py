from dataclasses import dataclass, field

from src.models import Transaction


@dataclass
class TransactionLedger:
    _transactions: list[Transaction] = field(default_factory=list)
