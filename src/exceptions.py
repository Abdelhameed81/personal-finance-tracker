from src.models import Transaction


class TransactionNotFoundError(Exception):
    def __init__(self, transaction: Transaction):
        super().__init__("This transaction does not exist in the ledger.")
        self.transaction = transaction
