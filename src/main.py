from pathlib import Path

from src.cli.app import run_app
from src.repositories.json_transaction_repository import JsonTransactionRepository
from src.services.transaction_service import TransactionService

project_root = Path(__file__).resolve().parent
json_file = project_root / "data/transactions.json"
repository = JsonTransactionRepository(json_file)
transaction_service = TransactionService(repository)
run_app(transaction_service)
