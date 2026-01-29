from typing import List
from src.database import Database
from src.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def create(
        self, from_address: str, to_address: str, amount: int, fee: int
    ) -> Transaction:
        pass

    def get_by_user(self, user_id: int) -> List[Transaction]:
        pass

    def get_by_wallet(self, address: str) -> List[Transaction]:
        pass

    def get_all(self) -> List[Transaction]:
        pass

    def get_total_fees(self) -> int:
        pass

    def get_total_count(self) -> int:
        pass

