from src.ledger import TransactionLedger


def test_ledger_transactions_is_unique_per_ledger_object():
    ledger_1 = TransactionLedger()
    ledger_2 = TransactionLedger()
    assert ledger_1._transactions is not ledger_2._transactions
