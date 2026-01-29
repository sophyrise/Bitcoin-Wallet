
from __future__ import annotations

from src.database import Database
from src.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def create(
        self, from_address: str, to_address: str, amount: int, fee: int
    ) -> Transaction:
        pass

    def get_by_user(self, user_id: int) -> list[Transaction]:
        pass

    def get_by_wallet(self, address: str) -> list[Transaction]:
        pass

    def get_all(self) -> list[Transaction]:
        pass

    def get_total_fees(self) -> int:
        pass

    def get_total_count(self) -> int:
        pass

