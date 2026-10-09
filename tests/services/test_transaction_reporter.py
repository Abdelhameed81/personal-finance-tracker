from src.models.ledger import TransactionLedger
from src.models.transaction import Transaction
from src.services.transaction_reporter import TransactionReporter


def test_empty_ledger(empty_ledger: TransactionLedger):
    transaction_reporter = TransactionReporter(empty_ledger.transactions)
    assert not transaction_reporter.income_transactions()


def test_one_income_ledger(one_income_ledger: TransactionLedger, valid_income_transaction: Transaction):
    transaction_reporter = TransactionReporter(one_income_ledger.transactions)
    assert transaction_reporter.income_transactions()[0] == valid_income_transaction


def test_one_expense_ledger(one_expense_ledger: TransactionLedger, valid_expense_transaction: Transaction):
    transaction_reporter = TransactionReporter(one_expense_ledger.transactions)
    assert transaction_reporter.expense_transactions()[0] == valid_expense_transaction


def test_multi_income_ledger(multi_income_ledger: TransactionLedger, valid_income_transaction: Transaction):
    transaction_reporter = TransactionReporter(multi_income_ledger.transactions)
    assert transaction_reporter.income_transactions() == (valid_income_transaction,) * 3


def test_multi_expense_ledger(multi_expense_ledger: TransactionLedger, valid_expense_transaction: Transaction):
    transaction_reporter = TransactionReporter(multi_expense_ledger.transactions)
    assert transaction_reporter.expense_transactions() == (valid_expense_transaction,) * 3


def test_mixed_transaction_ledger(mixed_transaction_ledger: TransactionLedger,
                                  valid_income_transaction: Transaction,
                                  valid_expense_transaction: Transaction):
    transaction_reporter = TransactionReporter(mixed_transaction_ledger.transactions)
    assert transaction_reporter.income_transactions() == (valid_income_transaction,) * 2
    assert transaction_reporter.expense_transactions() == (valid_expense_transaction,) * 2


def test_total_income(mixed_transaction_ledger: TransactionLedger, valid_income_transaction: Transaction):
    transactions = mixed_transaction_ledger.transactions
    transaction_reporter = TransactionReporter(transactions)
    assert transaction_reporter.total_income() == valid_income_transaction.amount * 2


def test_total_expenses(mixed_transaction_ledger: TransactionLedger, valid_expense_transaction: Transaction):
    transactions = mixed_transaction_ledger.transactions
    transaction_reporter = TransactionReporter(transactions)
    assert transaction_reporter.total_expenses() == valid_expense_transaction.amount * 2


def test_balance(mixed_transaction_ledger: TransactionLedger,
                 valid_income_transaction: Transaction,
                 valid_expense_transaction: Transaction):
    transactions = mixed_transaction_ledger.transactions
    transaction_reporter = TransactionReporter(transactions)
    assert transaction_reporter.balance == (valid_income_transaction.amount * 2 - valid_expense_transaction.amount * 2)
